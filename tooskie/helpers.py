from django.utils.text import slugify
import re

from tooskie.constants import LOGGING_CONFIG

import logging
logger = logging.getLogger("django")


def loop_to_remove_first_word(word_list, name):
    word = None
    if not isinstance(word_list, list):
        word_list = [word_list]
    for potential_word in word_list:
        if name.startswith(potential_word) and (name.replace(potential_word, '', 1)[0] == ' ' or potential_word[-1] == "'"):
            word = potential_word
            name = name[len(word):].strip()
            break
    return name, word

def update_or_create_then_save(model_class, data):
    logger.debug(data)
    created = False
    try:
        model_instance = model_class.objects.get(**data)
    except Exception as e:
        logger.debug(e)
        model_instance = model_class(**data)
        model_instance.save()
        created = True
    permaname = model_instance.permaname
    if created:
        logger.info(model_class.__name__ + ' ' + permaname + ' has been created\n')
    else:
        logger.info(model_class.__name__ + ' ' + permaname + ' was already in the database\n')
    return model_instance

def get_or_create(object_, permaname_):
    try:
        instance = object_.objects.get(permaname=permaname_)
        return instance, False
    except:
        instance = object_(permaname=permaname_)
        return instance, True

# Used to keep only a subset of keys of a dict
def get_sub_dict(old_dict, to_keep):
    if isinstance(to_keep, str):
        to_keep = [to_keep]
    new_dict = dict((k,old_dict[k]) for k in to_keep if k in old_dict)
    return new_dict

# Used to drop keys of a dict
def drop_columns(data, to_drop):
    try:
        if to_drop:
            if not isinstance(to_drop, list):
                to_drop = [to_drop]
            for key_to_drop in to_drop:
                data.pop(key_to_drop, None)
    except Exception as e:
        logger.error(e)
    return data

def remove_useless_spaces(string):
    return re.sub(' +', ' ', string)