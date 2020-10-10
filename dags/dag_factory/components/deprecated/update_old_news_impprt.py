import os
import glob
import logging

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

from dag_factory.components.old_news_import import OldNewsImportSpec
from dag_factory.components.utils import get_all_csv_paths, date_str_to_unixtime, tag_dict_to_dict
from newscrawler.crawler import extract_article_text_from_html
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

        for path in glob.glob(os.path.join(exec_properties["backup_dir"], "*")):
            csv_paths = get_all_csv_paths(path)
            print("Storing {} files to MongoDB".format(len(csv_paths)))
            for csv_path in csv_paths:
                if "NewsCrawler" in csv_path:
                    csv_rel_path = os.path.relpath(csv_path, os.path.join(path, "pipelines"))
                    csv_rel_path_norm = os.path.normpath(csv_rel_path)
                    csv_source = csv_rel_path_norm.split(os.sep)[0]
                    csv_source = csv_source.replace(".py", "")

                    col = db[csv_source]
                    try:
                        df = pd.read_csv(csv_path)
                    except:
                        continue
                    logging.info("--Storing {} files to {} from {}".format(len(df),
                                                                           csv_source, csv_path))
                    for _, row in df.iterrows():
                        data = dict(row)
                        try:
                            article_information = extract_article_information_from_html(get_page(data["link"]))
                            if len(data["text"]) < len(article_information["text"]):
                                data["text"] = article_information["text"]
                            data["published"] = date_str_to_unixtime(data["published"])
                            data["tags"] = tag_dict_to_dict(data["tags"])
                        except:
                            pass

                        data_op = {'$set': data}
                        query = {'link': data['link']}
                        col.update_one(query, data_op, upsert=True)
                        logging.info("\tWorking on: {}".format(data['link']))


class UpdateOldNewsImport(base_component.BaseComponent):
    SPEC_CLASS = OldNewsImportSpec
    EXECUTOR_SPEC = executor_spec.ExecutorClassSpec(Executor)

    def __init__(self,
                 backup_dir: Text,
                 ip: Text = None,
                 port: Text = None,
                 username: Text = None,
                 password: Text = None,
                 dbname: Text = None):
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

        spec = OldNewsImportSpec(ip=ip,
                                 port=port,
                                 username=username,
                                 password=password,
                                 dbname=dbname,
                                 backup_dir=backup_dir)

        super(UpdateOldNewsImport, self).__init__(spec=spec)
