import os
import yaml
import time
import logging

import pandas as pd

from datetime import datetime

from typing import Any, Dict, List, Text

from tfx import types

from tfx.components.base import base_component
from tfx.components.base import executor_spec
from tfx.components.base import base_executor

from tfx.types import standard_artifacts

from tfx.types.artifact_utils import get_single_uri

from tfx.types.component_spec import ChannelParameter
from tfx.types.component_spec import ExecutionParameter

from tfx.utils.dsl_utils import external_input


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


class Executor(base_executor.BaseExecutor):

    def Do(self, input_dict: Dict[Text, List[types.Artifact]],
           output_dict: Dict[Text, List[types.Artifact]],
           exec_properties: Dict[Text, Any]) -> None:
        input_path = os.path.join(get_single_uri(input_dict["rss_feed"]), "feed.csv")
        news_df = pd.read_csv(input_path)

        logging.info(news_df.head())
        news_df["published"] = [date_str_to_unixtime(date_str) for date_str in news_df["published"]]
        news_df["tags"] = [tag_dict_to_dict(tag_dict) for tag_dict in news_df["tags"]]
        logging.info(news_df.head())

        output_path = os.path.join(get_single_uri(output_dict["rss_feed_cleaned"]), "feed.csv")
        news_df.to_csv(output_path, index=False)


class NewsCleanerSpec(types.ComponentSpec):
    PARAMETERS = {
    }

    INPUTS = {
        'rss_feed': ChannelParameter(type=standard_artifacts.ExternalArtifact),
    }

    OUTPUTS = {
        'rss_feed_cleaned': ChannelParameter(type=standard_artifacts.ExternalArtifact),
    }


class NewsCleaner(base_component.BaseComponent):
    SPEC_CLASS = NewsCleanerSpec
    EXECUTOR_SPEC = executor_spec.ExecutorClassSpec(Executor)

    def __init__(self,
                 rss_feed: types.Channel):
        rss_feed_cleaned = external_input("rss_feed")
        spec = NewsCleanerSpec(rss_feed_cleaned=rss_feed_cleaned,
                               rss_feed=rss_feed)

        super(NewsCleaner, self).__init__(spec=spec)
