import json
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.text import slugify
from fractions import Fraction

from tooskie.recipe.models import Recipe, Ingredient, Measurement, MeasureOfIngredient, DifficultyLevel, BudgetLevel, Step, Ustensil, UstensilInRecipe, IngredientInRecipe, Measurement, MeasureOfIngredient
from tooskie.recipe.serializers import RecipeSerializer
from tooskie.utils.models import Tag
from tooskie.helpers import get_sub_dict, loop_to_remove_first_word, update_or_create_then_save, drop_columns

import logging
from tooskie.constants import LOGGING_CONFIG, UNITS_MARMITON, LINKING_WORD_MARMITON

logging.basicConfig(**LOGGING_CONFIG)


class PopulateConfig:
    LEVEL_MODELS = [
        'difficulty_level',
        'budget_level'
    ]

    RECIPE_FIELDS = {
        'recipe': 'name',
        'url': 'url',
        'cooking_time': 'cooking_time',
        'preparation_time': 'preparation_time'
    }

    MEASUREMENT_FIELDS = [
        'unit', 
        'unit_plural'
    ]

    INGREDIENT_FIELDS = [
        'picture',
        'name',
        'name_plural',
        'complement', 
        'complement_plural'
    ]

    MEASURE_OF_INGREDIENT_FIELDS = [
        'linking_word',
        'linking_word_plural'
    ]

    KEY_TO_MODEL = {
        'steps': Step,
        'tags': Tag,
        'difficulty_level': DifficultyLevel,
        'budget_level': BudgetLevel,
        'ustensils': Ustensil,
        'ustensils_in_recipe': UstensilInRecipe,
        'ingredient': Ingredient,
        'ingredient_in_recipe': IngredientInRecipe,
        'measurement': Measurement,
        'measure_of_ingredient': MeasureOfIngredient
    }

def get_data(data_file='data/marmiton_scrap_2.json', recipe_number=1):
    with open(data_file) as f:
        data = json.load(f)
    global_data = data[str(recipe_number)]
    return global_data

def process_recipe(global_data):
    logging.debug(global_data["recipe"])
    try:
        recipe_data = get_fields(global_data)
        update_or_create_then_save(Recipe, recipe_data)
    except Exception as e:
        logging.error(e)

def get_fields(global_data):
    try:
        recipe_data = format_recipe_dict(global_data)
        recipe_model = update_or_create_then_save(Recipe, recipe_data)
        recipe_data.update(create_levels(global_data))
        create_steps(global_data, recipe_model)
        create_tags(global_data, recipe_model)
        create_ustensils(global_data, recipe_model)
        create_ingredients(global_data, recipe_model)
        return recipe_data
    except Exception as e:
        logging.error('Creation or update of recipe ' + recipe_data['name'] + ' failed')
        raise e

def create_levels(global_data):
    models_dict = {}
    for level_type in PopulateConfig.LEVEL_MODELS:
        try:
            level_data = {
                'name': global_data[level_type]
            }
            model = create_model(level_type, level_data)
            models_dict[level_type] = model
        except Exception as e:
            logging.error(e)
    return models_dict

def create_steps(global_data, recipe_model):
    step_list = []
    for step in global_data['steps']:
        step['permaname'] = slugify(str(recipe_model) + ' ' + str(step['step_number']))
        step_list.append(step)
    global_data['steps'] = step_list
    create_model_list(global_data, 'steps', recipe_model=recipe_model)

def create_tags(global_data, recipe_model):
    tag_to_dict = []
    for tag in global_data['tags']:
        tag_to_dict.append({'name': tag, 'model_tagged': 'Recipe'})
    global_data['tags'] = tag_to_dict
    tag_list = create_model_list(global_data, 'tags')
    for tag in tag_list:
        recipe_model.tag.add(tag)

def create_ustensils(global_data, recipe_model):
    logging.info('Creation or update of the different ustensils')
    ustensils_to_dict = []
    ustensils_in_recipe_to_dict = []
    for ustensil in global_data['ustensils']:
        name_split = ustensil['name'].split(' ')
        quantity = int(name_split[0])
        name = ' '.join(name_split[1:]).capitalize()
        ustensils_to_dict.append({
            'name': name,
            'picture': ustensil['picture']
        })
        ustensils_in_recipe_to_dict.append({
            'quantity': quantity,
            'permaname': slugify(recipe_model.permaname + ' ' + name),
            'recipe': recipe_model
        })
    global_data['ustensils'] = ustensils_to_dict
    ustensils_list = create_model_list(global_data, 'ustensils')
    for i in range(len(ustensils_list)):
        ustensils_in_recipe_to_dict[i]['ustensil'] = ustensils_list[i]
    global_data['ustensils_in_recipe'] = ustensils_in_recipe_to_dict
    create_model_list(global_data, 'ustensils_in_recipe')

def create_ingredients(global_data, recipe_model):
    people_number = float(Fraction(global_data['people_number']))
    global_data['ingredient'] = []
    global_data['measurement'] = [] 
    global_data['measure_of_ingredient'] = []
    global_data['ingredient_in_recipe'] = []
    for ingredient_data in global_data['ingredients']:
        logging.debug(ingredient_data)
        ingredient_data.update(format_ingredient(ingredient_data))
        logging.debug(ingredient_data)
        global_data['measurement'].append(get_sub_dict(ingredient_data, PopulateConfig.MEASUREMENT_FIELDS))
        global_data['ingredient'].append(get_sub_dict(ingredient_data, PopulateConfig.INGREDIENT_FIELDS))
        global_data['measure_of_ingredient'].append(get_sub_dict(ingredient_data, PopulateConfig.MEASURE_OF_INGREDIENT_FIELDS))
        if ingredient_data['quantity'] != "null":
            quantity = float(Fraction(ingredient_data['quantity'])) / people_number
            global_data['ingredient_in_recipe'].append({
                'quantity': quantity
            })
    measurement_list = create_model_list(global_data, 'measurement')
    ingredient_list = create_model_list(global_data, 'ingredient')
    for i in range(len(measurement_list)):
        global_data['measure_of_ingredient'][i]['measurement'] = measurement_list[i]
        global_data['measure_of_ingredient'][i]['ingredient'] = ingredient_list[i]
    measure_of_ingredient_list = create_model_list(global_data, 'measure_of_ingredient')
    for i in range(len(measure_of_ingredient_list)):
        global_data['ingredient_in_recipe'][i]['measure_of_ingredient'] = measure_of_ingredient_list[i]
        global_data['ingredient_in_recipe'][i]['recipe'] = recipe_model

def format_ingredient(ingredient):
    try:
        name_dict = format_ingredient_name(ingredient['name'])
        logging.debug(name_dict)
        name_dict.update(format_ingredient_name_plural(ingredient['name_plural'], name_dict))
        if not name_dict['unit']:
            name_dict['unit'] = 'none'
    except Exception as e:
        logging.error('Formatting of ingredient failed')
        raise e
    return name_dict

def format_ingredient_name(name):
    name, unit = loop_to_remove_first_word(UNITS_MARMITON, name)
    linking_word = None
    if unit:
        name, linking_word = loop_to_remove_first_word(LINKING_WORD_MARMITON, name)
    name = name.capitalize()
    final_dict = {}
    for i in ('name', 'unit', 'linking_word'):
        final_dict[i] = locals()[i]
    return final_dict

def format_ingredient_name_plural(name_plural, name_dict):
    if not name_dict['unit']:
        if name_dict['linking_word']:
            logging.debug(name_dict)
        return {}
    logging.debug('Name plural')
    logging.debug(name_dict)
    name_plural_temp = name_plural[len(name_dict['unit']):]
    name_plural_temp = name_plural_temp.split(name_dict['linking_word'])
    unit_plural = name_plural[:len(name_dict['unit']) + len(name_plural_temp[0])].strip()
    name_plural = name_dict['linking_word'].join(name_plural_temp[1:]).strip().capitalize()
    final_dict = {}
    for i in ('name_plural', 'unit_plural'):
        final_dict[i] = locals()[i]
    return final_dict
             
def create_model_list(global_data, key, to_drop=None, recipe_model=None):
    logging.info('Create model list: ' + key)
    model_list = []
    for data in global_data[key]:
        try:
            drop_columns(data, to_drop)
            model = create_model(key, data, global_data['recipe'], recipe_model=recipe_model)
            model_list.append(model)
        except Exception as e:
            logging.error(e)
    return model_list

def create_model(model_key, model_data, recipe_name=None, recipe_model=None):
    logging.info('Create model: ' + model_key)
    try:
        model_class = PopulateConfig.KEY_TO_MODEL[model_key]
        if recipe_model:
            model_data['recipe'] = recipe_model
        model = update_or_create_then_save(model_class, model_data)
    except Exception as e:
        logging.error('Creation of the model failed')
        logging.error(e)
        raise e
    return model

def format_recipe_dict(global_data):
    logging.debug('Format recipe dict')
    logging.debug(global_data)
    recipe_data = get_sub_dict(global_data, PopulateConfig.RECIPE_FIELDS.keys())
    logging.debug(recipe_data)
    for key, value in PopulateConfig.RECIPE_FIELDS.items():
        if key != value:
            recipe_data[value] = recipe_data[key]
            recipe_data.pop(key, None)
        if value[-5:] == '_time':
            if 'h' in recipe_data[value]:
                time_split = recipe_data[value].strip().split('h')
                time = int(time_split[0].strip()) * 60 + int(time_split[1].strip())
            elif 'min' in recipe_data[value]:
                time = int(recipe_data[value].replace('min', '').strip())
            else:
                logging.error(recipe_data[value] + " isn't a valid format")
                raise ValueError('Time formatting failed')
            recipe_data[value] = time
    logging.debug('Format recipe dict done')
    return recipe_data
    
data = get_data()
process_recipe(data)

