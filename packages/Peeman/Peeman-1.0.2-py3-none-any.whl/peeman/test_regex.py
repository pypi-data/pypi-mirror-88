
import os
import re
import json
import logging


regex_pattern =r'[^{]\{\{([^{}]+)\}\}[^}]'


def check_regex_unique(regex_pattern, data):
    match = re.findall(regex_pattern, json.dumps(data))
    return (list(set(match)))


def replace_string(replace_dict, data):
    for string_to_replace, value in replace_dict.items():
        replace_pattern = '(\{\{' + string_to_replace + '\}\})'
        replace_pattern_complied = re.compile(replace_pattern)
        data = re.sub(replace_pattern_complied, value, data)
    return data


def write_json(filename, data):
    with open(filename, "w") as outfile:
        outfile.write(data)


def get_place_holders(data_string):
    placeholders = None
    try:
        data_string = json.dumps(data_string)
        placeholders = check_regex_unique(regex_pattern, data_string)
    except Exception as err:
        logging.error(err)
        raise err
    return placeholders


def place_holder_check_replace(data_string, list_replace):
    placeholders = None
    data_string = json.dumps(data_string)
    flag_replace = True
    placeholders = check_regex_unique(regex_pattern, data_string)
    if list_replace and placeholders:
        for placeholder in placeholders:
            if not placeholder in list_replace:
                flag_replace = False
                break
    elif placeholders and not list_replace:
        flag_replace = False
        raise Exception(f"please provide the following placeholder value : {placeholders}")
    elif not (placeholders and list_replace):
        flag_replace = True
    else:
        flag_replace = False
        raise Exception("error in input commands , please check again.")
    return flag_replace
    

def replace_placeholders(data, list_replace):
    data_string = json.dumps(data)
    final_data = replace_string(list_replace, data_string)
    return json.loads(final_data)
