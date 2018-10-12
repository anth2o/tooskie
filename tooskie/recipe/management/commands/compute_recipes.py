from django.core.management.base import BaseCommand, CommandError
from tooskie.pantry.generate_recipes import get_recipes
from tooskie.constants import RECIPE_PICKLE
import pickle

class Command(BaseCommand):
    help = 'Generate the pickle object'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        recipes = get_recipes()
        print(recipes)
        pickle.dump(recipes, open(RECIPE_PICKLE, "wb"))
    