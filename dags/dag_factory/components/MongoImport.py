import os
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


def get_all_csv_paths(path):
    csv_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".csv"):
                csv_paths.append(os.path.join(root, file))
    return csv_paths


class Executor(base_executor.BaseExecutor):

    def Do(self, input_dict: Dict[Text, List[types.Artifact]],
           output_dict: Dict[Text, List[types.Artifact]],
           exec_properties: Dict[Text, Any]) -> None:
        client = MongoClient(host=exec_properties["ip"],
                             port=int(exec_properties["port"]),
                             username=exec_properties["username"],
                             password=exec_properties["password"])
        db = client[exec_properties["dbname"]]

        output_path = get_single_uri(input_dict["rss_feed"])
        csv_paths = get_all_csv_paths(output_path)
        logging.info("Storing {} files to MongoDB".format(len(csv_paths)))
        for csv_path in csv_paths:
            col = db[exec_properties["colname"]]

            df = pd.read_csv(csv_path)
            print("--Storing {} files to {}".format(len(df), exec_properties["colname"]))
            for _, row in df.iterrows():
                data = dict(row)
                data_op = {'$set': data}
                query = {'link': data['link']}
                col.update_one(query, data_op, upsert=True)


class MongoImportSpec(types.ComponentSpec):
    PARAMETERS = {
        'ip': ExecutionParameter(type=Text),
        'port': ExecutionParameter(type=Text),
        'username': ExecutionParameter(type=Text),
        'password': ExecutionParameter(type=Text),
        'dbname': ExecutionParameter(type=Text),
        'colname': ExecutionParameter(type=Text),
    }

    INPUTS = {
        'rss_feed': ChannelParameter(type=standard_artifacts.ExternalArtifact),
    }

    OUTPUTS = {
    }


class MongoImport(base_component.BaseComponent):
    SPEC_CLASS = MongoImportSpec
    EXECUTOR_SPEC = executor_spec.ExecutorClassSpec(Executor)

    def __init__(self,
                 rss_feed: types.Channel,
                 colname: Text,
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

        spec = MongoImportSpec(ip=ip,
                               port=port,
                               username=username,
                               password=password,
                               dbname=dbname,
                               rss_feed=rss_feed,
                               colname=colname)

        super(MongoImport, self).__init__(spec=spec)
