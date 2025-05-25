from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook # api hook
from airflow.providers.postgres.hooks.postgres import PostgresHook # postgresdb hook
from airflow.decorators import task # help to make ETL pipline, automativaly detect
import json
import pendulum
start_date = pendulum.now("UTC").subtract(days=1)

