from django.core.management.base import BaseCommand, CommandError
from tooskie.populate import populate_db, populate_db_one_recipe

class Command(BaseCommand):
    help = 'Populate database from scrapped data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--recipe_id',
            dest='recipe_id',
            help='Populate a specific recipe',
        )
    def handle(self, *args, **options):
        if 'recipe_id' in options and options['recipe_id']:
            for recipe_id in options['recipe_id']:
                populate_db_one_recipe(recipe_id)
        else:
            populate_db()
    