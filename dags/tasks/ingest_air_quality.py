# dags/tasks/ingest_air_quality.py

import requests
from airflow.decorators import task
from utils.cities import cities

@task()
def ingest_air_quality():
    results = []

    for city in cities:
        lat = city["lat"]
        lon = city["lon"]
        nombre = city["city"]
        estado = city["state"]

        url = (
            "https://air-quality-api.open-meteo.com/v1/air-quality"
            f"?latitude={lat}&longitude={lon}"
            "&hourly=pm10,pm2_5,ozone,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide"
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
                "air_quality_raw": data
            })

        except Exception as e:
            print(f"Error al consultar Open-Meteo para {nombre}, {estado}: {e}")
            results.append({
                "city": nombre,
                "state": estado,
                "lat": lat,
                "lon": lon,
                "air_quality_raw": None,
                "error": str(e)
            })

    return results
