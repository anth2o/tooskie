from django.utils.text import slugify

from tooskie.constants import LOGGING_CONFIG

import logging
logging.basicConfig(**LOGGING_CONFIG)


def loop_to_remove_first_word(word_list, name):
    word = None
    if not isinstance(word_list, list):
        word_list = [word_list]
    for potential_word in word_list:
        if name.startswith(potential_word):
            word = potential_word
            name = name[len(word):].strip()
            break
    return name, word

def update_or_create_then_save(model_class, data):
    try:
        permaname = None
        if 'name' in data:
            permaname = slugify(data['name'])
        elif 'permaname' in data:
            permaname = data['permaname']
        elif 'unit' in data
            permaname = data['unit']
        else:
            raise Exception('No permaname given')
        model_instance = model_class.objects.get(permaname=permaname)
        to_create = False
    except Exception as e:
        to_create = True
    try:
        if to_create:
            model_instance = model_class.objects.create(**data)
            logging.info(model_class.__name__ + ' ' + permaname + ' has been created\n')
        else:
            # models = model_class.objects.filter(permaname=model_instance.permaname)
            model_instance.__dict__.update(data)
            logging.info(model_class.__name__ + ' ' + permaname + ' has been updated\n')
        model_instance.save()
    except Exception as e:
        logging.error(e)
        raise e
    return model_instance

# Used to keep only a subset of keys of a dict
def get_sub_dict(old_dict, to_keep):
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
        logging.error(e)
    return data