# dags/tasks/ingest_openweather.py

import os
import requests
from airflow.decorators import task
from utils.cities import cities

@task()
def ingest_openweather():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("La variable de entorno 'OPENWEATHER_API_KEY' no está definida.")

    results = []

    for city in cities:
        nombre = city["openweather_name"] if "openweather_name" in city else city["city"]
        estado = city["state"]

        # Formato: Ciudad + País (para evitar ambigüedad)
        query = f"{nombre},MX"

        url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={query}&appid={api_key}&units=metric"
        )

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            results.append({
                "city": nombre,
                "state": estado,
                "openweather_raw": data
            })

        except Exception as e:
            print(f"Error al consultar OpenWeather para {nombre}, {estado}: {e}")
            results.append({
                "city": nombre,
                "state": estado,
                "openweather_raw": None,
                "error": str(e)
            })

    return results
