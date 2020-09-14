import os

from dag_factory.components.old_news_import import OldNewsImport
from dag_factory.components.news_crawler import NewsCrawler
from dag_factory.components.mongo_import import MongoImport
from dag_factory.components.news_cleaner import NewsCleaner

from tfx.orchestration import metadata
from tfx.orchestration import pipeline

from tfx.orchestration.airflow.airflow_dag_runner import AirflowDagRunner
from tfx.orchestration.airflow.airflow_dag_runner import AirflowPipelineConfig


def create_dag(name, url, airflow_config, dag_type="default", output_dir="/output"):
    pipeline_name = name.replace(".py", "")
    pipeline_root = os.path.join(output_dir, 'pipelines', pipeline_name)
    metadata_path = os.path.join(output_dir, 'metadata', pipeline_name,
                                 'metadata.db')

    components = []
    if dag_type == "default":
        crawler = NewsCrawler(url=url)
        mongo = MongoImport(
            rss_feed=crawler.outputs["rss_feed"], colname=pipeline_name)
        components = components + [crawler, mongo]
    elif dag_type == "cleaner":
        crawler = NewsCrawler(url=url)
        cleaner = NewsCleaner(rss_feed=crawler.outputs["rss_feed"])
        mongo = MongoImport(
            rss_feed=cleaner.outputs["rss_feed_cleaned"], colname=pipeline_name)
        components = components + [crawler, cleaner, mongo]
    elif dag_type == "backup":
        old_news = OldNewsImport(backup_dir="/output/pipelines_backup")

        components = components + [old_news]

    airflow_config["catchup"] = False
    tfx_pipeline = pipeline.Pipeline(pipeline_name=pipeline_name,
                                     pipeline_root=pipeline_root,
                                     components=components,
                                     enable_cache=False,
                                     metadata_connection_config=metadata.sqlite_metadata_connection_config(
                                         metadata_path))

    return AirflowDagRunner(AirflowPipelineConfig(airflow_config)).run(tfx_pipeline)
