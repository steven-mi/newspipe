import os
import datetime

from dag_factory import create_dag

airflow_config = {'schedule_interval': None,  # every 30 minutes
                  # year, month, day, hour
                  'start_date': datetime.datetime(2020, 7, 6, 21),
                  }

DAG = create_dag(url=None,
                 airflow_config=airflow_config,
                 name=os.path.basename(__file__),
                 dag_type="update",
                 mongo_ip="127.0.0.1")
