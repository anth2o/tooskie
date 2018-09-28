import os
import logging

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
    'cL',
    'L',
    'cuillère à café',
    'cuillère à soupe',
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
    'botte'
]

# If any questions on the code, ask Boubou or Schmoulou

NONE_UNIT = 'None'
NONE_MEASURE = 'Count'