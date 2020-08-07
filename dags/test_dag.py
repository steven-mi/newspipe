import os

from dag_factory import create_dag

url = "bild.de"
airflow_config = {'schedule_interval': None}

DAG = create_dag(url=url,
                 airflow_config=airflow_config,
                 name=os.path.basename(__file__))
