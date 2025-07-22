# dags/tasks/ingest_geonames.py

import os
import requests
from airflow.decorators import task
from utils.cities import cities  # Asegúrate que cities.py esté en utils/

@task()
def ingest_geonames():
    username = os.getenv("GEONAMES_USERNAME")
    if not username:
        raise ValueError("La variable de entorno 'GEONAMES_USERNAME' no está definida.")

    results = []

    for city in cities:
        lat = city["lat"]
        lon = city["lon"]
        nombre = city["city"]
        estado = city["state"]

        url = (
            f"http://api.geonames.org/findNearbyPlaceNameJSON"
            f"?lat={lat}&lng={lon}&username={username}"
        )

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            results.append({
                "city": nombre,
                "state": estado,
                "lat": lat,
                "lon": lon,
                "geonames_raw": data
            })

        except Exception as e:
            print(f"Error al consultar GeoNames para {nombre}, {estado}: {e}")
            results.append({
                "city": nombre,
                "state": estado,
                "lat": lat,
                "lon": lon,
                "geonames_raw": None,
                "error": str(e)
            })

    return results  # Esto se guarda en XCom para ser usado por la siguiente tarea
