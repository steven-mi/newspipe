# NewsPipe
This repository contains the complete pipeline for collecting online newspaper article. The articles are stored to MongoDB. The whole pipeline is dockerized, thus the user does not need to worry about dependencies. Additionally, docker-compose is available to increase the useability for the user.

## Requirement
To use this system, you need to create a `.env` file in which the MongoDB information is available:

```
MONGO_ROOT_USER=devroot
MONGO_ROOT_PASSWORD=devroot
MONGOEXPRESS_LOGIN=dev
MONGOEXPRESS_PASSWORD=dev
POSTGRES_USER=airflow
POSTGRES_PASS=airflow
RABBITMQ_USER=rabbit
RABBITMQ_PASS=rabbit
```

If you want to specify the number of threads then open `airflow-newspipe-docker` and adjust the sed command in line 57 e.g. if you want 4 threads:
```
&& sed -i'.orig' 's/max_threads = 2/max_threads = 4/g' ${AIRFLOW_HOME}/airflow.cfg \
```
or 10:
```
&& sed -i'.orig' 's/max_threads = 2/max_threads = 10/g' ${AIRFLOW_HOME}/airflow.cfg \
```
It is recommended to set the number of threads to the number of available cores.

## Getting Started
To start this application, run:
```
docker-compose up airflow-newspipe
```
To add worker nodes, run:
```
docker-compose up airflow-worker
```
To run have multiple worker nodes on a single machine, run:
```
docker-compose up --scale airflow-worker=<N_WORKERS>
```

- To see the database collections, [mongo-express](https://github.com/mongo-express/mongo-express) is in use and available on `localhost:8081`. The MongoDB itself is available on port `27017`. 
- The airflow application should be available on `localhost:8080`. You will see the airflow dashboard with the default examples.
- The RabbitMQ webapp is available on `localhost:15672`. There you can see all the worker nodes and their status.

## Adding article sources
Each crawler is defined as DAG in 'dag'. To add a data source, you must therefore add DAGs in the `dags` folder. A DAG is a Python script that contains the settings for an entire crawling pipeline. Use the default example as a template. The DAGs are very simple and straightforward.

```python
import os
import datetime

from dag_factory import create_dag

url = "taz.de" # url of newspaper source

# defining the crawling times
airflow_config = {'schedule_interval': '@hourly', # set a interval, for continuous crawling
                  'start_date': datetime.datetime(2020, 6, 4, 21), # set a date, on which the dag will run
                  'end_date':datetime.datetime(2020, 6, 5, 6), # optinal, set if it is needed
                  }

# create DAG
DAG = create_dag(url=url,
                 airflow_config=airflow_config,
                 name=os.path.basename(__file__))
```
Options for `schedule_interval`:
| preset       | meaning                                                    | cron          |
| ------------ | ---------------------------------------------------------- | ------------- |
| `@once`      | Schedule once and only once                                |               |
| `@hourly`    | Run once an hour at the beginning of the hour              | `0 * * * *`   |
| `@daily`     | Run once a day at midnight                                 | `0 0 * * *`   |
| `@weekly`    | Run once a week at midnight on Sunday morning              | `0 0 * * 0`   |
| `@monthly`   | Run once a month at midnight of the first day of the month | `0 0 1 * *`   |
| `@quarterly` | Run once a quarter at midnight on the first day            | `0 0 1 */3 *` |
| `@yearly`    | Run once a year at midnight of January 1                   | `0 0 1 1 *`   |


