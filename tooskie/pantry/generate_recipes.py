from tooskie.pantry.models import Pantry, IngredientInPantry
from tooskie.recipe.models import Recipe, Ingredient, UnitOfIngredient, IngredientInRecipe
from tooskie.constants import RECIPE_PICKLE
import pickle

def get_ingredients(pantry):
    ingredients = []
    for ingredient_in_pantry in pantry.ingredients_in_pantry.all():
        ingredients.append(ingredient_in_pantry.unit_of_ingredient.ingredient)
    return ingredients

def get_recipes():
    recipes = Recipe.objects.all()
    recipe_list = []
    for recipe in recipes:
        recipe_dict = {
            'recipe': recipe,
            'ingredients': []
        }
        ingredients_in_recipe = recipe.unit_of_ingredient.all()
        for ingredient_in_recipe in ingredients_in_recipe:
            recipe_dict['ingredients'].append(ingredient_in_recipe.ingredient)
        recipe_list.append(recipe_dict)
    return recipe_list

def get_recipes_pickle():
    return pickle.load(open(RECIPE_PICKLE, "rb"))

def filter_recipes(ingredients, recipe_list):
    recipe_to_keep = []
    for recipe in recipe_list:
        if set(recipe['ingredients']).issubset(set(ingredients)) and recipe['ingredients'] != []:
            recipe_to_keep.append(recipe['recipe'])
    return recipe_to_keep
