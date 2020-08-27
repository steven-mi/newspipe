#!/bin/bash
rm /airflow/airflow-webserver*.pid
airflow webserver -D
airflow scheduler
