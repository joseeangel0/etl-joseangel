# dags/tasks/load_to_mongodb.py

from airflow.decorators import task
from pymongo import MongoClient
import datetime

@task()
def load_to_mongodb(transformed_data, geonames_data, openweather_data, air_quality_data):
    try:
        # Conexión al MongoDB corriendo en Docker (puerto 27018)
        client = MongoClient("host.docker.internal", 27018)
        db = client["clima_db"]
        
        #Colecciones
        collection = db["ciudades_clima"]
        geonames_raw_col = db["geonames_raw"]
        openweather_raw_col = db["openweather_raw"]
        air_quality_raw_col = db["air_quality_raw"]

        # Insertamos con timestamp para seguimiento
        for doc in transformed_data:
            doc["ingested_at"] = datetime.datetime.utcnow()
        for doc in geonames_data:
            doc["ingested_at"] = datetime.datetime.utcnow()
        for doc in openweather_data:
            doc["ingested_at"] = datetime.datetime.utcnow()
        for doc in air_quality_data:
            doc["ingested_at"] = datetime.datetime.utcnow()

        collection.insert_many(transformed_data)
        geonames_raw_col.insert_many(geonames_data)
        openweather_raw_col.insert_many(openweather_data)
        air_quality_raw_col.insert_many(air_quality_data)

        print(f"✔ Insertados {len(transformed_data)} documentos en MongoDB.")
    except Exception as e:
        print(f"❌ Error al insertar en MongoDB: {e}")
