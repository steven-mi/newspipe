import os
import yaml
import time
from datetime import datetime

def get_all_csv_paths(path):
    csv_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".csv"):
                csv_paths.append(os.path.join(root, file))
    return csv_paths


def date_str_to_unixtime(date_str):
    d = None
    try:
        d = datetime.strptime(date_str)
    except:
        pass
    try:
        d = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
    except:
        pass
    try:
        d = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    except:
        pass
    try:
        d = datetime.strptime(date_str.split(
            '+')[0].replace("T", " "), '%Y-%m-%d %H:%M:%S')
    except:
        pass
    try:
        d = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    except:
        pass
    try:
        d = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except:
        pass
    return time.mktime(d.timetuple())


def tag_dict_to_dict(tag_dict):
    tags = []

    tag_list = yaml.load(tag_dict)
    if isinstance(tag_list, list):
        for tag in tag_list:
            tags.append(tag["term"])
        return tags
    return None
