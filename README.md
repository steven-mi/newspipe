# NewsPipe
This repository contains the complete pipeline for crawling online newspaper article. The articles are stored to MongoDB. The whole pipeline is dockerized, thus the user does not need to worry about dependencies. Additionally, docker-compose is available to increase the useability for the user.


## Requirement
To use this system, you need to create a `.env` file in which the MongoDB information is available:

```
MONGO_ROOT_USER=devroot
MONGO_ROOT_PASSWORD=devroot
MONGOEXPRESS_LOGIN=dev
MONGOEXPRESS_PASSWORD=dev
```

## Getting Started
To start this application, run:
```
docker-compose up
```
- To see the database collections, [mongo-express](https://github.com/mongo-express/mongo-express) is in use and available on `localhost:8081`. The MongoDB itself is available on port `27017`. 
- The airflow application should be available on `localhost:8080`. You will see the airflow dashboard with our default examples:


## Adding new article sources
The crawler dags are defined in `dags`. A DAG contains the settings for a whole crawling pipeline. Therefore to add/remove a pipeline, you will have to add/remove DAGs in the `dags` folder. Please use one of the default example as template. The DAGs are very simple and straightforward.

```python
import os
import datetime

from dag_factory import create_dag

url = "taz.de" # Online newspaper source

# defining the crawling times
airflow_config = {'schedule_interval': '@hourly',
                  'start_date': datetime.datetime(2020, 6, 4, 21),
                  'end_date':datetime.datetime(2020, 6, 5, 6), # optinal, set if it is needed
                  }

# create DAG
DAG = create_dag(url=url,
                 airflow_config=airflow_config,
                 name=os.path.basename(__file__))
```


