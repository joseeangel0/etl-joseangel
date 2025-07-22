# dags/tasks/transform_data.py

from airflow.decorators import task
from datetime import timedelta

@task(retries=1, retry_delay=timedelta(minutes=1))
def transform_data(geonames_data, air_quality_data, openweather_data):
    transformed = []

    # Aseguramos que cada lista tenga la misma cantidad de ciudades y estén en el mismo orden
    for geo, air, weather in zip(geonames_data, air_quality_data, openweather_data):
        city = geo["city"]
        state = geo["state"]

        # GeoNames info (puede venir vacía)
        geo_info = geo.get("geonames_raw", {}).get("geonames", [{}])[0]
        country = geo_info.get("countryName", "Desconocido")
        admin = geo_info.get("adminName1", "Desconocido")

        # Air quality hourly info
        air_data = air.get("air_quality_raw", {}).get("hourly", {})
        aq_index = {}
        for pollutant in ["pm10", "pm2_5", "ozone"]:
            values = air_data.get(pollutant, [])
            if values:
                valid_values = [v for v in values if v is not None]
                if valid_values:
                    avg = sum(valid_values) / len(valid_values)
                else:
                    avg = None
                aq_index[pollutant] = round(avg, 2)
            else:
                aq_index[pollutant] = None

        # OpenWeather info

        weather_data = weather.get("openweather_raw", {}) or {}

        print(f"[INFO] Procesando ciudad: {city}")
        print(f"[DEBUG] weather_data: {weather_data}")

        temp = weather_data.get("main", {}).get("temp")
        humidity = weather_data.get("main", {}).get("humidity")
        precipitation = weather_data.get("rain", {}).get("1h", 0)
        condition = weather_data.get("weather", [{}])[0].get("description", "Desconocido")


        # Reglas para alertas
        alerts = []
        if temp is not None and temp > 35:
            alerts.append("Calor extremo")
        if precipitation is not None and precipitation > 10:
            alerts.append("Lluvia intensa")
        if aq_index.get("pm2_5") is not None and aq_index["pm2_5"] > 55:
            alerts.append("Alta contaminación PM2.5")


        


        # Resultado final
        lat = geo["lat"] if "lat" in geo else None
        lon = geo["lon"] if "lon" in geo else None

        transformed.append({
            "city": city,
            "state": state,
            "country": country,
            "admin_area": admin,
            "temperature": temp,
            "humidity": humidity,
            "precipitation_mm": precipitation,
            "weather_condition": condition,
            "air_quality": aq_index,
            "alerts": alerts,
            "latitude": lat,
            "longitude": lon
        })

    return transformed
