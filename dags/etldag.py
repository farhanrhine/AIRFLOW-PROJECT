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
LOCATIONS = [
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
) as dag: # all above hold in one variable dag
    
    @task()# task define when which one run
    # 1st task Extract 
    def extract_weather_date():
        http_hook = HttpHook(http_conn_id= API_CONN_ID, method='GET') # connect api
        weather_data_list = [] #empty list so when reponse came its store

# how i want to store and what
        for location in LOCATIONS:  # location hold my latitude & longitude
            endpoint = (
                f"/v1/forecast?"
                f"latitude={location['latitude']}&"
                f"longitude={location['longitude']}&"
                f"current_weather=true"
            )

            response = http_hook.run(endpoint) # store after api hitted by me 

            if response.status_code == 200 : # indicate ok , responce successfully
                data = response.json()
                data['location'] = location
                weather_data_list.append(data)
            else:
                raise Exception('Failed to Fetch data')
            
        return weather_data_list ## store Extracted data : in weather_data_list 

    
# 2nd task  Transform 
    @task()
    def transform_weather_data(weather_data_list):
        
        transform_data_list = []

        for data in weather_data_list:
            current_weather = data['current_weather']
            location = data['location']

            transformed_data = {
                'latitude' : location['latitude'],
                'longitude' : location['longitude'],
                'temperature': current_weather['temperature'],
                'windspeed': current_weather['windspeed'],
                'winddirection' : current_weather['winddirection'],
                'weathercode': current_weather['weathercode']
            }

            transform_data_list.append(transformed_data)

        return transform_data_list # Transformed data store in transform_data_list
    
# 3rd task Load data

    @task
    def load_weather_data(transform_data_list):
        pg_hook = PostgresHook(Postgres_conn_id = POSTGES_CONN_ID) # make hook
        conn = pg_hook.get_conn() # connect hook

        cursor = conn.cursor() # cursor helps to write sql queries within python 

        # create table
        cursor.execute("""

                CREATE TABLE IF NOT EXISTS weather_data(
                       latitude  FLOAT,
                       longitude FLOAT,
                       temperature FLOAT,
                       windspeed FLOAT,
                       winddirection FLOAT,
                       weathercode FLOAT,
                       timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       );


                       """)
        # insert queries in table
        for record in transform_data_list:
            cursor.execute("""

                    INSERT INTO weather_data(latitude, longitude, temperature, windspeed, winddirection, weathercode)
                    VALUES(%s, %s, %s, %s, %s, %s);

                          """, (
                              record['latitude'],
                              record['longitude'],
                              record['temperature'],
                              record['windspeed'],
                              record['winddirection'],
                              record['weathercode']
                          )
                          )
        conn.commit() # run both queries
        conn.close() 

    ### work-flow ETL pipe-line
    weather_data_list = extract_weather_date() # Extract data from API
    transform_data_list = transform_weather_data(weather_data_list) #Transform data json to postgreldb
    load_weather_data(transform_data_list) # Load data from postgreldb



        


            


    
    


