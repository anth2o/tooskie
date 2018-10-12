from django.core.management.base import BaseCommand, CommandError
from tooskie.pantry.generate_recipes import save_recipes_pickle
from tooskie.constants import RECIPE_PICKLE
import pickle

class Command(BaseCommand):
    help = 'Generate the pickle object'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        save_recipes_pickle()
    