from django.utils.text import slugify
from django.db.models import Model
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

def get_or_create_from_data(model_class, data):
    logger.debug(data)
    created = False
    data_ic = get_ic_dictionary(data)
    logger.debug(data_ic)
    try:
        model_instance = model_class.objects.get(**data_ic)
    except Exception:
        model_instance = model_class(**data)
        try:
            model_instance.save()
            created = True
        except Exception:
            try:
                if 'name' in data:
                    model_instance = model_class.objects.get(name__iexact=data['name'])
                else:
                    model_instance = model_class.objects.get(**keep_model_values(data))
            except Exception as e:
                logger.error("Model {} hasn't been created because there is already an instance with the same name".format(model_class))
                logger.error(data)
                raise e
    permaname = model_instance.permaname
    if created:
        logger.info(model_class.__name__ + ' ' + permaname + ' has been created\n')
    else:
        logger.info(model_class.__name__ + ' ' + permaname + ' was already in the database\n')
    return model_instance

def get_ic_dictionary(data):
    data_ic = {}
    try:
        for key, value in data.items():
            if isinstance(value, str):
                data_ic[key + '__iexact'] = value
            else:
                data_ic[key] = value
    except Exception as e:
        logger.error(data)
        logger.error(e)
        raise e
    return data_ic

def keep_model_values(data):
    res = {}
    for key, value in data.items():
        if isinstance(value, Model):
            res[key] = value
    return res

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

def add_suffix(data, keys, suffixes):
    new_data = data.copy()
    for key, value in data.items():
        if key in keys:
            for suffix in suffixes:
                new_data[key + '_' + suffix] = value
            new_data.pop(key)
    return new_data
