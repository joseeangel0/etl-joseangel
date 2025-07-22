# DAG principal con 5 tareas: 3 ingestas, 1 transformación, 1 carga
# dags/dag_clima_etl.py

from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import timedelta

# Importar tasks
from tasks.ingest_geonames import ingest_geonames
from tasks.ingest_air_quality import ingest_air_quality
from tasks.ingest_openweather import ingest_openweather
from tasks.transform_data import transform_data
from tasks.load_to_mongodb import load_to_mongodb

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='clima_etl_multiciudad',
    description='ETL que unifica clima, aire y geolocalización por ciudad',
    schedule_interval='@hourly',  # Puedes cambiar a None para ejecución manual
    start_date=days_ago(1),
    catchup=False,
    default_args=default_args,
    tags=['etl', 'clima', 'mongo']
) as dag:

    # Ejecutar tasks
    t1 = ingest_geonames()
    t2 = ingest_air_quality()
    t3 = ingest_openweather()

    t4 = transform_data(t1, t2, t3)

    t5 = load_to_mongodb(t4, t1, t3, t2)  # <-- Aquí pasamos los datos raw también

    # Definir orden de ejecución
    [t1, t2, t3] >> t4 >> t5
