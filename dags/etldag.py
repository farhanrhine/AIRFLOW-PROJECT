# ETL pip line 
from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook # api hook
from airflow.providers.postgres.hooks.postgres import PostgresHook # postgresdb hook
from airflow.decorators import task # help to make ETL pipline, automativaly detect
import json
import pendulum

# 1. set configure
#start_date = pendulum.now("UTC").subtract(days=1)

# variables
LOCATION = [
    {'latitude': '51.5074', 'longitude' : '-0.1278'}, # london
    {'latitude': '40.7128', 'longitude' : '-74.0064'}, # new york
    {'latitude': '48.8566', 'longitude' : '2.3522'} # paris
]

POSTGES_CONN_ID  = "postgres_default"
API_CONN_ID = "open_meteo_api"

default_args ={
    'owner': 'farhan',
    #'start_date' : start_date,
    'start_date' : pendulum.now("UTC").subtract(days=1),
    'retries' : 1 # if failed then re-run 1 times

}

with DAG(
    dag_id='multi_location_weather_etl',
    default_args=default_args,
    schedule = '@daily', # AUTOMATIC daily update
    catchup= False # by default its True, [if False , only run current date , ignore previous date]
)


