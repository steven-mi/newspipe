import os
    import datetime

    from dag_factory import create_dag

    
url = "butzbacher-zeitung.de"

    airflow_config = {'schedule_interval': '*/30 * * * *', # every 30 minutes
                      'start_date': datetime.datetime(2020, 7, 6, 21), # year, month, day, hour
                      }

    DAG = create_dag(url=url,
                     airflow_config=airflow_config,
                     name=os.path.basename(__file__))