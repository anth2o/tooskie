import json
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.text import slugify

from tooskie.recipe.models import Recipe, Ingredient, Measurement, MeasureOfIngredient, DifficultyLevel, BudgetLevel, Step
from tooskie.recipe.serializers import RecipeSerializer
from tooskie.utils.models import Tag

import logging
from tooskie.constants import LOGGING_CONFIG

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

    KEY_TO_MODEL = {
        'ingredients': Ingredient,
        'steps': Step,
        'tags': Tag,
        'difficulty_level': DifficultyLevel,
        'budget_level': BudgetLevel
    }

def get_data(data_file='data/marmiton_scrap_2.json', recipe_number=0):
    with open(data_file) as f:
        data = json.load(f)
    global_data = data[str(recipe_number)]
    return global_data

def process_recipe(global_data):
    logging.debug(global_data["recipe"])
    try:
        recipe_data = get_fields(global_data)
        recipe_model, created = Recipe.objects.update_or_create(**recipe_data)
        recipe_model.save()
    except Exception as e:
        logging.error(e)

def update_or_create_then_save(model_class, data):
    try:
        if 'name' in data:
            permaname = slugify(data['name'])
        else:
            permaname = data['permaname']
        model_instance = model_class.objects.get(permaname=permaname)
        to_create = False
    except Exception as e:
        to_create = True
    try:
        if to_create:
            model_instance = model_class.objects.create(**data)
            logging.info(model_class.__name__ + ' ' + permaname + ' has been created\n')
        else:
            model_class.objects.filter(id=model_instance.id).update(**data)
            logging.info(model_class.__name__ + ' ' + permaname + ' has been updated\n')
        model_instance.save()
    except Exception as e:
        logging.error(e)
        raise e
    return model_instance

def get_fields(global_data):
    try:
        recipe_data = format_recipe_dict(global_data)
        recipe_model = update_or_create_then_save(Recipe, recipe_data)
        recipe_data.update(create_levels(global_data))
        # create_model_list(global_data, 'ingredients', to_drop=['quantity'])
        create_steps(global_data, recipe_model)
        create_tags(global_data, recipe_model)
        return recipe_data
    except Exception as e:
        raise ValueError({"error":"OBJECT UPDATE FAILED", "info":str(e)})

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
    logging.debug('Level models correctly saved\n')
    return models_dict

def create_steps(global_data, recipe_model):
    logging.debug('Beginning creation of steps')
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

def create_model_list(global_data, key, to_drop=None, recipe_model=None):
    logging.debug('Create model list: ' + key)
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

def drop_columns(data, to_drop):
    try:
        if to_drop:
            if not isinstance(to_drop, list):
                to_drop = [to_drop]
            for key_to_drop in to_drop:
                data.pop(key_to_drop, None)
    except Exception as e:
        logging.error(e)
    return data

def format_recipe_dict(global_data):
    logging.debug('Format recipe dict')
    recipe_data = dict((k,global_data[k]) for k in PopulateConfig.RECIPE_FIELDS.keys() if k in global_data)
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

