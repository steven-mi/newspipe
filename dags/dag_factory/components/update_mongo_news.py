import os
import glob
import logging

import numpy as np
import pandas as pd

from pymongo import MongoClient
from typing import Any, Dict, List, Text

from tfx import types

from tfx.components.base import base_component
from tfx.components.base import executor_spec
from tfx.components.base import base_executor

from tfx.types import standard_artifacts

from tfx.types.artifact_utils import get_single_uri

from tfx.types.component_spec import ChannelParameter
from tfx.types.component_spec import ExecutionParameter

from dag_factory.components.utils import get_all_csv_paths, date_str_to_unixtime, tag_dict_to_dict
from newscrawler.crawler import extract_article_information_from_html
from newscrawler.extract_rss import get_page


class Executor(base_executor.BaseExecutor):

    def Do(self, input_dict: Dict[Text, List[types.Artifact]],
           output_dict: Dict[Text, List[types.Artifact]],
           exec_properties: Dict[Text, Any]) -> None:
        client = MongoClient(host=exec_properties["ip"],
                             port=int(exec_properties["port"]),
                             username=exec_properties["username"],
                             password=exec_properties["password"])
        db = client[exec_properties["dbname"]]

        updated_collections = exec_properties["updated_collections"]
        update_collections = exec_properties["update_collections"]

        collection_names = [collection for collection in client["NewsPipe"].collection_names()]

        for collection_name in collection_names:
            if updated_collections and collection_name in updated_collections:
                print("{} already updated".format(collection_name))
                continue
            if update_collections and collection_name not in update_collections:
                print("{} not in update_collections - skipping collection")
                continue

            print("working on {}".format(collection_name))
            collection = db[collection_name]

            processed = 0
            while True:
                cursor = collection.find({}, no_cursor_timeout=True).skip(processed)
                try:
                    for document in cursor:
                        document_link = document["link"]

                        # Date
                        unixtime = date_str_to_unixtime(document["published"])
                        if unixtime:
                            document["published"] = unixtime
                        # Tags
                        try:
                            tag_str = tag_dict_to_dict(document["tags"])
                            if tag_str:
                                document["tags"] = tag_str
                        except:
                            print("{} couldn't be parsed".format(tag_str))

                        try:
                            article_html = get_page(document_link)
                            article_information = extract_article_information_from_html(article_html)
                            # Text
                            if document["text"] != document["text"] or not document["text"] or len(document["text"]) < len(article_information["text"]):
                                document["text"] = article_information["text"]
                            # Author
                            if document["author"] != document["author"] or not document["author"]:
                                document["author"] = article_information["author"]
                        except Exception as e:
                            print(document_link)
                            print(e)

                        data_op = {'$set': document}
                        query = {'link': document['link']}
                        print("Updating: {}".format(document_link))
                        collection.update_one(query, data_op, upsert=True)
                        processed += 1
                    break
                except Exception as e:
                    print("Lost cursor. Retry")
                    print(e)


class UpdateMongoNewsSpec(types.ComponentSpec):
    PARAMETERS = {
        'ip': ExecutionParameter(type=Text),
        'port': ExecutionParameter(type=Text),
        'username': ExecutionParameter(type=Text),
        'password': ExecutionParameter(type=Text),
        'dbname': ExecutionParameter(type=Text),
        'backup_dir': ExecutionParameter(type=Text),
        'update_collections': ExecutionParameter(type=List),
        'updated_collections': ExecutionParameter(type=List),
    }

    INPUTS = {
    }

    OUTPUTS = {
    }


class UpdateMongoNews(base_component.BaseComponent):
    SPEC_CLASS = UpdateMongoNewsSpec
    EXECUTOR_SPEC = executor_spec.ExecutorClassSpec(Executor)

    def __init__(self,
                 ip: Text = None,
                 port: Text = None,
                 username: Text = None,
                 password: Text = None,
                 dbname: Text = None,
                 updated_collections: List = [],
                 update_collections: List = []):

        if not ip:
            ip = "mongo"
        if not port:
            port = "27017"
        if not username:
            username = os.environ['MONGO_ROOT_USER']
        if not password:
            password = os.environ['MONGO_ROOT_PASSWORD']
        if not dbname:
            dbname = os.environ['MONGO_DATABASE_NAME']

        spec = UpdateMongoNewsSpec(ip=ip,
                                   port=port,
                                   username=username,
                                   password=password,
                                   dbname=dbname,
                                   update_collections=update_collections,
                                   updated_collections=updated_collections,
                                   backup_dir="")

        super(UpdateMongoNews, self).__init__(spec=spec)
