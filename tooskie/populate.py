import json
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.text import slugify
from fractions import Fraction

from tooskie.recipe.models import Recipe, Ingredient, Unit, UnitOfIngredient, DifficultyLevel, BudgetLevel, Step, Ustensil, UstensilInRecipe, IngredientInRecipe
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
        'preparation_time': 'preparation_time',
        'picture': 'picture'
    }

    UNIT_FIELDS = [
        'unit', 
        'unit_plural'
    ]

    INGREDIENT_FIELDS = [
        'picture',
        'name',
        'name_plural'
    ]

    INGREDIENT_IN_RECIPE_FIELDS = [
        'complement', 
        'complement_plural'
    ]

    UNIT_OF_INGREDIENT_FIELDS = [
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
        'unit': Unit,
        'unit_of_ingredient': UnitOfIngredient
    }

def get_data_file(data_file='data/marmiton_scrap.json'):
    with open(data_file) as f:
        data = json.load(f)
    return data

def populate_db():
    data = get_data_file()
    for i in range(len(data)):
        try:
            recipe_data = data[str(i)]
            process_recipe(recipe_data)
        except Exception:
            pass

def populate_db_one_recipe(recipe_number=0):
    data = get_data_file()
    recipe_data = data[str(recipe_number)]
    process_recipe(recipe_data)


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
        levels = create_levels(global_data)
        recipe_model.difficulty_level = levels['difficulty_level']
        recipe_model.budget_level = levels['budget_level']
        recipe_model.save()
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
        try:
            quantity = int(name_split[0])
        except Exception:
            logging.error('Quantity is not Integer')
            continue
        name = ' '.join(name_split[1:]).capitalize()
        if name[-6:].lower() != 'amazon':
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
    global_data = format_global_data_for_ingredient(global_data)
    unit_list = create_model_list(global_data, 'unit')
    ingredient_list = create_model_list(global_data, 'ingredient')
    for i in range(len(unit_list)):
        global_data['unit_of_ingredient'][i]['unit'] = unit_list[i]
        global_data['unit_of_ingredient'][i]['ingredient'] = ingredient_list[i]
    unit_of_ingredient_list = create_model_list(global_data, 'unit_of_ingredient')
    for i in range(len(unit_of_ingredient_list)):
        global_data['ingredient_in_recipe'][i]['unit_of_ingredient'] = unit_of_ingredient_list[i]
        global_data['ingredient_in_recipe'][i]['recipe'] = recipe_model
    create_model_list(global_data, 'ingredient_in_recipe')

def format_global_data_for_ingredient(global_data):
    if global_data['people_number'] == '':
        people_number = None
    else:
        people_number = float(Fraction(global_data['people_number']))
    global_data['ingredient'] = []
    global_data['unit'] = [] 
    global_data['unit_of_ingredient'] = []
    global_data['ingredient_in_recipe'] = []
    for ingredient_data in global_data['ingredients']:
        ingredient_data.update(format_ingredient(ingredient_data))
        unit_dict = get_sub_dict(ingredient_data, PopulateConfig.UNIT_FIELDS)
        unit_dict['name'] = unit_dict.pop('unit')
        if 'unit_plural' in unit_dict:
            unit_dict['name_plural'] = unit_dict.pop('unit_plural')
        global_data['unit'].append(unit_dict)
        global_data['ingredient'].append(get_sub_dict(ingredient_data, PopulateConfig.INGREDIENT_FIELDS))
        global_data['unit_of_ingredient'].append(get_sub_dict(ingredient_data, PopulateConfig.UNIT_OF_INGREDIENT_FIELDS))
        quantity = None
        if ingredient_data['quantity'] != "null" and ingredient_data['quantity'] != "" and people_number:
            quantity = float(Fraction(ingredient_data['quantity'])) / people_number
        ingredient_in_recipe_dict = get_sub_dict(ingredient_data, PopulateConfig.INGREDIENT_IN_RECIPE_FIELDS)
        ingredient_in_recipe_dict.update({'quantity': quantity})
        global_data['ingredient_in_recipe'].append(ingredient_in_recipe_dict)
    logging.debug('Formatting of global data for ingredients succeeded')
    return global_data

def format_ingredient(ingredient):
    try:
        name_dict = format_ingredient_name(ingredient['name'])
        name_dict.update(format_ingredient_name_plural(ingredient['name_plural'], name_dict))
    except Exception as e:
        logging.error('Formatting of ingredient failed')
        raise e
    return name_dict

def format_ingredient_name(name):
    unit = ''
    name, unit = loop_to_remove_first_word(UNITS_MARMITON, name)
    linking_word = ''
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
    try:
        recipe_data = get_sub_dict(global_data, PopulateConfig.RECIPE_FIELDS.keys())
        logging.debug(recipe_data)
        for key, value in PopulateConfig.RECIPE_FIELDS.items():
            if key != value:
                recipe_data[value] = recipe_data[key]
                recipe_data.pop(key, None)
            if value[-5:] == '_time':
                if recipe_data[value] == 'none':
                    time = None
                elif 'h' in recipe_data[value]:
                    time_split = recipe_data[value].strip().split('h')
                    if time_split[1].strip() == '':
                        time = int(time_split[0].strip()) * 60
                    else:
                        time = int(time_split[0].strip()) * 60 + int(time_split[1].strip())
                elif 'min' in recipe_data[value]:
                    time = int(recipe_data[value].replace('min', '').strip())
                else:
                    logging.error(recipe_data[value] + " isn't a valid format")
                    raise ValueError('Time formatting failed')
                recipe_data[value] = time
        logging.debug('Format recipe dict done')
    except Exception as e:
        logging.error(e)
        raise e
    return recipe_data
