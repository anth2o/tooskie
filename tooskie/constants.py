import os
import logging
from django.conf import settings

LINK_WORD = ' in '
LOGGING_LEVEL = os.environ['LOGGING_LEVEL']
LOGGING_CONFIG = {
    "format": '[%(asctime)s] [%(levelname)s] : %(message)s',
    "level": logging.getLevelName(LOGGING_LEVEL),
    "datefmt": '%d/%b/%Y %H:%M:%S'
    }

LINKING_WORD_MARMITON = [
    'de',
    "d'"
]

UNITS_MARMITON = [
    'g',
    'kg',
    'mL',
    'cL',
    'L',
    'ml',
    'cl',
    'l',
    'cuillère à café',
    'cuillère à café rase',
    'cuillère à soupe',
    'cuillère à soupe rase',
    'pincée',
    'brin',
    'branche',
    'feuille',
    'gousse',
    'sachet',
    'boîte',
    'grande boîte',
    'petite boîte',
    'brolivmax',
    'botte',
    'rouleau',
    'cuillère',
    'grand verre',
    'verre',
    'petit verre',
    'poignée',
    'barquette',
    'tranche', 
    'plaque',
    'trait',
    'cube',
    'bouquet',
    'gros bouquet',
    'pot',
    'paquet',
    'tranche',
    'fine tranche',
    'tranche fine',
    'boule',
    'demi',
    'bouteille',
    'pavé',
    'filet',
    'tasse',
    'pot',
    'grand pot',
    'petit pot',
    'poignée',
    'dose',
    'pousse',
    'goutte',
    'brique',
    'morceau',
    'bâton'
]

# If any questions on the code, ask Boubou or Schmoulou

NONE_UNIT = 'None'

RECIPE_PICKLE = settings.BASE_DIR + '/recipes.pickle'
