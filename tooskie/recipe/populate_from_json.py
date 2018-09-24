import json
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from tooskie.recipe.models import Recipe, Ingredient, Measurement, MeasureOfIngredient, DifficultyLevel, BudgetLevel
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

def get_data(data_file='data/marmiton_scrap_2.json', recipe_number=0):
    with open(data_file) as f:
        data = json.load(f)

    global_data = data[str(recipe_number)]

    return global_data

def process_recipe(global_data):
    logging.info(global_data["recipe"])
    try:
        recipe_model = Recipe.objects.get(name=global_data["recipe"])
        logging.info("Recipe already exists, updating it")
        update_recipe(global_data)
    except ObjectDoesNotExist:
        logging.info("Recipe doesn't exists, creating it")
        create_recipe(global_data) 

def update_recipe(global_data):
    try:
        serializer = RecipeSerializer(global_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except Exception as e:
        raise ValueError({"error":"OBJECT UPDATE FAILED", "info":str(e)})   

def create_recipe(global_data):
    try:
        recipe_data = format_recipe_dict(global_data)
        recipe_model = Recipe(**recipe_data)
        recipe_model.save()
        create_levels(global_data)
        create_ingredients(global_data)
        # recipe_model = Recipe(**recipe_data)
        # recipe_model.save()
    except Exception as e:
        raise ValueError({"error":"OBJECT UPDATE FAILED", "info":str(e)})

def create_model(model_class, model_data):
    try:
        logging.debug(model_data)
        name = model_data['name']
        logging.info(name)
        level_model = model_class.objects.get(name=name)
    except Exception as e:
        logging.info(str(model_class.__name__) + ' ' + str(name) + " doesn't exist, creating it")
        level_model = model_class(**model_data)
        try:
            level_model.save()
        except Exception as e:
            logging.error('Creation of the model failed')
            raise e

def create_levels(global_data):
    for level_type, level_model_class in LEVEL_TYPE_TO_MODEL.items():
        try:
            level_data = {
                'name': global_data[level_type]
            }
            create_model(level_model_class, level_data)
        except Exception as e:
            logging.error(e)
    
def create_ingredients(global_data):
    for ingredient_data in global_data['ingredients']:
        try:
            ingredient_data.pop('quantity', None)
            create_model(Ingredient, ingredient_data)
        except Exception as e:
            logging.error(e)


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

