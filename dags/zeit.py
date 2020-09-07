import os
import datetime

from dag_factory import create_dag

# first dag --------------------------
url = "https://newsfeed.zeit.de/all"
airflow_config = {'schedule_interval': '*/30 * * * *',  # every 30 minutes
                  # year, month, day, hour
                  'start_date': datetime.datetime(2020, 7, 6, 21),
                  }
globals()[0] = create_dag(url=url,
                          airflow_config=airflow_config,
                          name=os.path.basename(__file__))

# second dag --------------------------
url = "https://newsfeed.zeit.de"
airflow_config = {'schedule_interval': '*/30 * * * *',  # every 30 minutes
                  # year, month, day, hour
                  'start_date': datetime.datetime(2020, 7, 6, 21),
                  }
globals()[1] = create_dag(url=url,
                          airflow_config=airflow_config,
                          name=os.path.basename(__file__))
