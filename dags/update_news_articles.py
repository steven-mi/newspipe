import os
import datetime

from dag_factory import create_dag

airflow_config = {'schedule_interval': None,  # every 30 minutes
                  # year, month, day, hour
                  'start_date': datetime.datetime(2020, 7, 6, 21),
                  }

already_updated = ["esslinger-zeitung",
                   "berliner-zeitung",
                   "express",
                   "fehmarn24",
                   "focus",
                   "gandersheimer-kreisblatt",
                   "goettinger-tageblatt",
                   "handelsblatt",
                   "kornwestheimer-zeitung",
                   "weser-kurier",
                   "zeit",
                   "heise",
                   "kn-online",
                   "waz-online",
                   "torgauerzeitung",
                   "spiegel",
                   "tag24",
                   "wz",
                   "giessener-allgemeine",
                   "hersfelder-zeitung",
                   "stuttgarter-zeitung",
                   "chrismon",
                   "landeszeitung",
                   "hertener-allgemeine",
                   "bz-berlin",
                   "mainpost",
                   "idowa",
                   "deutsche-handwerks-zeitung",
                   "kevelaerer-blatt",
                   "gmuender-tagespost",
                   "taz",
                   "tagesspiegel",
                   "kurier",
                   "lahrer-zeitung",
                   "hanauer",
                   "ikz-online",
                   "kreiszeitung",
                   "faz",
                   "dnn",
                   "thueringer-allgemeine",
                   "wetterauer-zeitung",
                   "haller-kreisblatt",
                   "welt"]

DAG = create_dag(url=None,
                 airflow_config=airflow_config,
                 name=os.path.basename(__file__),
                 dag_type="update",
                 mongo_ip="127.0.0.1",
                 updated_collections=already_updated)
