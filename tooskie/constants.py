import os
import logging

LINK_WORD = '-'
LOGGING_LEVEL = os.environ['LOGGING_LEVEL']
LOGGING_CONFIG = {
    "format": '[%(asctime)s] [%(levelname)s] : %(message)s',
    "level": logging.getLevelName(LOGGING_LEVEL),
    "datefmt": '%d/%b/%Y %H:%M:%S'
}

LINKING_WORD_MARMITON = [
    'de ',
    'd'
]   