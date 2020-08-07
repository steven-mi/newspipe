import os
import time
import yaml

import pandas as pd

from datetime import datetime
from pymongo import MongoClient


CSV_PATH = "/output/pipeline_backup"
DB_NAME = os.environ['MONGO_DATABASE_NAME']

IP = "0.0.0.0"
PORT = 27017

USERNAME = os.environ['MONGO_ROOT_USER']
PASSWORD = os.environ['MONGO_ROOT_PASSWORD']


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
        d = datetime.strptime(date_str.split('+')[0].replace("T", " "), '%Y-%m-%d %H:%M:%S')
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


def get_all_csv_paths(path):
    csv_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".csv"):
                csv_paths.append(os.path.join(root, file))
    return csv_paths


def main():
    client = MongoClient(IP, PORT, username=USERNAME, password=PASSWORD)
    db = client[DB_NAME]

    csv_paths = get_all_csv_paths(CSV_PATH)
    print("Storing {} files to MongoDB".format(len(csv_paths)))
    for csv_path in csv_paths:
        csv_rel_path = os.path.relpath(csv_path, CSV_PATH)
        csv_rel_path_norm = os.path.normpath(csv_rel_path)
        csv_source = csv_rel_path_norm.split(os.sep)[0]

        col = db[csv_source]

        df = pd.read_csv(csv_path)
        df["published"] = [date_str_to_unixtime(date_str) for date_str in df["published"]]
        df["tags"] = [tag_dict_to_dict(tag_dict) for tag_dict in df["tags"]]

        print("--Storing {} files to {}".format(len(df), csv_source))
        for _, row in df.iterrows():
            data = dict(row)
            data_op = {'$set': data}
            query = {'link': data['link']}
            col.update_one(query, data_op, upsert=True)

if __name__ == '__main__':
    print("Start reading CSV files to MongoDB")
    main()