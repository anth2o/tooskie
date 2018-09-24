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

def get_data(data_file='data/marmiton_scrap_2.json', recipe_number=0):
    with open(data_file) as f:
        data = json.load(f)

    recipe_data = data[str(recipe_number)]

    return recipe_data


def process_recipe(recipe_data):
    logging.info(recipe_data["recipe"])
    try:
        recipe_data['name'] = recipe_data['recipe']
        recipe_model = Recipe.objects.get(name=recipe_data["recipe"])
        logging.info("Object already exists, updating it")
        update_recipe(recipe_data)
    except ObjectDoesNotExist:
        logging.info("Object doesn't exists, creating it")
        create_recipe(recipe_data) 

def update_recipe(recipe_data):
    try:
        serializer = RecipeSerializer(recipe_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except Exception as e:
        raise ValueError({"error":"OBJECT UPDATE FAILED", "info":str(e)})   

def create_recipe(recipe_data):
    try:
        for level_type, level_model_class in LEVEL_TYPE_TO_MODEL.items():
            try:
                create_level(level_model_class, recipe_data[level_type])
            except Exception as e:
                logging.error(e)
        # recipe_model = Recipe(**recipe_data)
        # recipe_model.save()
    except Exception as e:
        raise ValueError({"error":"OBJECT UPDATE FAILED", "info":str(e)}) 

def create_level(level_model_class, level_data):
    try:
        level_model = level_model_class.objects.get(name=level_data['name'])
    except Exception as e:
        logging.info(str(level_model_class.__name__) + ' ' + str(level_data) + ' ' + "doesn't exist, creating it")
        level_model = level_model_class(name=level_data)
        try:
            level_model.save()
        except Exception as e:
            logging.error('Creation of the model failed')
            raise e

data = get_data()
logging.warning(data)
process_recipe(data)

