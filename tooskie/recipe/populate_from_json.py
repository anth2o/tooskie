import json
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from tooskie.recipe.models import Recipe, Ingredient, Measurement, MeasureOfIngredient, DifficultyLevel, BudgetLevel, Step
from tooskie.recipe.serializers import RecipeSerializer
from tooskie.utils.models import Tag

import logging
from tooskie.constants import LOGGING_CONFIG

logging.basicConfig(**LOGGING_CONFIG)

LEVEL_TYPE_TO_MODEL = {
    "difficulty_level": DifficultyLevel,
    "budget_level": BudgetLevel
}

RECIPE_FIELDS = {
    'recipe': 'name',
    'url': 'url',
    'cooking_time': 'cooking_time',
    'preparation_time': 'preparation_time'
}

KEY_TO_MODEL = {
    'ingredients': Ingredient,
    'steps': Step
}

def get_data(data_file='data/marmiton_scrap_2.json', recipe_number=0):
    with open(data_file) as f:
        data = json.load(f)

    global_data = data[str(recipe_number)]

    return global_data

def process_recipe(global_data):
    logging.info(global_data["recipe"])
    try:
        recipe_data, model_has_recipe_fk = get_fields(global_data)
        logging.info(recipe_data)
        logging.info(model_has_recipe_fk)
        recipe_model, created = Recipe.objects.update_or_create(**recipe_data)
        recipe_model.save()
    except Exception as e:
        logging.error(e)

def get_fields(global_data):
    try:
        recipe_data = format_recipe_dict(global_data)
        recipe_model, created = Recipe.objects.update_or_create(**recipe_data)
        if created:
            logging.info('Recipe ' + str(recipe_data['name'] + ' has been created'))
        else:
            logging.info('Recipe ' + str(recipe_data['name'] + ' has been updated'))
        recipe_data.update(create_levels(global_data))
        create_model_list(global_data, 'ingredients', to_drop=['quantity'])
        model_has_recipe_fk = create_model_list(global_data, 'steps', recipe_model=recipe_model)
        return recipe_data, model_has_recipe_fk
    except Exception as e:
        raise ValueError({"error":"OBJECT UPDATE FAILED", "info":str(e)})

def create_model(model_key, model_data, recipe_name=None, recipe_model=None):
    try:
        logging.info('Create model')
        logging.info(model_key)
        model_class = KEY_TO_MODEL[model_key]
        name = get_model_name(model_key, model_data, recipe_name)
        logging.info(name)
        if recipe_model:
            model_data['recipe'] = recipe_model
        logging.info(model_data)
        try:
            model = model_class.objects.get(name=name)
            # model = model_class.objects.update(**model_data)
            created = False
        except:
            model = model_class(**model_data)
            created = True
        if created:
            logging.info(str(model_class) + ' ' + name + ' has been created')
        else:
            logging.info(str(model_class) + ' ' + name + ' has been updated')
        logging.info(model)
        model.save()
    except Exception as e:
        logging.error('Creation of the model failed')
        raise e
    return model

def get_model_name(model_key, model_data, recipe_name):
    if model_key == 'steps':
        name = recipe_name + ' ' + str(model_data['step_number'])
    else:
        name = model_data['name']
    return name

def create_levels(global_data):
    model_dict = {}
    for level_type, level_model_class in LEVEL_TYPE_TO_MODEL.items():
        try:
            level_data = {
                'name': global_data[level_type]
            }
            model = create_model(level_model_class, level_data)
            model_dict[level_type] = model
        except Exception as e:
            logging.error(e)
    return model_dict

def create_model_list(global_data, key, to_drop=None, recipe_model=None):
    logging.info('Create model list')
    logging.info(key)
    model_list = []
    for data in global_data[key]:
        try:
            drop_colums(data, to_drop)
            model = create_model(key, data, global_data['recipe'], recipe_model=recipe_model)
            logging.info(model)
            model_list.append(model)
        except Exception as e:
            logging.error(e)
    logging.info(model_list)
    return model_list
        

def drop_colums(data, to_drop):
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
    recipe_data = dict((k,global_data[k]) for k in RECIPE_FIELDS.keys() if k in global_data)
    for key, value in RECIPE_FIELDS.items():
        if key != value:
            recipe_data[value] = recipe_data[key]
            recipe_data.pop(key, None)
        logging.debug(value)
        if value[-5:] == '_time':
            logging.debug(recipe_data[value])
            if 'h' in recipe_data[value]:
                time_split = recipe_data[value].strip().split('h')
                time = int(time[0].strip()) * 60 + int(time[1].strip())
            elif 'min' in recipe_data[value]:
                time = int(recipe_data[value].replace('min', '').strip())
            else:
                logging.error(recipe_data[value] + " isn't a valid format")
                raise ValueError('Time formatting failed')
            recipe_data[value] = time
    return recipe_data
    
data = get_data()
logging.warning(data)
process_recipe(data)

