import json
from django.db.utils import IntegrityError

from tooskie.recipe.models import Recipe

import logging
from tooskie.constants import LOGGING_CONFIG

logging.basicConfig(**LOGGING_CONFIG)

def get_data(data_file='data/marmiton_scrap_2.json', recipe_number=0):
    with open(data_file) as f:
        data = json.load(f)

    recipe_data = data[str(recipe_number)]

    return recipe_data


def create_recipe(recipe_data):
    logging.info(recipe_data["recipe"])
    try:
        recipe_model = Recipe.objects.get_or_create(name=recipe_data["recipe"], url=recipe_data["url"])
        logging.info(recipe_model)
    except IntegrityError:
        logging.warning("The recipe " + str(recipe_data["recipe"] + " is already in DB"))
    

data = get_data()
logging.warning(data)
create_recipe(data)

