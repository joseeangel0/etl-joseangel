# Documentación del proyecto
# Environmental Data ETL Project – José Ángel Pech Xool

This project implements a complete ETL (Extract, Transform, Load) pipeline using Apache Airflow and Docker, designed to collect and unify environmental data from multiple APIs. It targets five Mexican cities and provides insightful dashboards through Streamlit and MongoDB.

---

## Objective

The goal of this project is to gather, process, and visualize data related to:

- 🌡️ Current weather conditions
- 🧪 Air pollution indicators (PM10, PM2.5, Ozone)
- 📍 Geographic metadata (state, country, coordinates)

The final result is a Streamlit dashboard that updates hourly and provides a friendly interface to explore environmental conditions across selected cities in Mexico.

---

## Tech Stack

| Tool | Purpose |
| ---- | ------- |
| **Python**    | Core scripting and data processing            |
| **Airflow**   | Workflow orchestration (DAGs, Tasks)          |
| **MongoDB**   | NoSQL database for storing raw and clean data |
| **Docker**    | Containerization of all services              |
| **Streamlit** | Interactive dashboard frontend                |
| **Plotly**    | Visualizations (maps, charts)                 |
| **Pandas**    | Data manipulation                             |

---

## Folder Structure

etl-joseangel/
│
├── dags/
│   ├── main_pipeline.py           # Central Airflow DAG
│   ├── tasks/
│   │   ├── ingest_geonames.py     # Ingest GeoNames API
│   │   ├── ingest_openweather.py  # Ingest OpenWeather API
│   │   ├── ingest_air_quality.py  # Ingest Open-Meteo API
│   │   ├── transform_data.py      # Data cleaning/transformation
│   │   └── load_to_mongodb.py     # Load to MongoDB
│   └── utils/
│       ├── cities.py              # Target cities (lat, lon, names)
│       └── mongo_utils.py         # MongoDB connection helpers
│
├── app.py                         # Streamlit dashboard
├── Dockerfile                     # Streamlit container
├── requirements.txt               # Python dependencies
├── docker-compose.yml             # Multi-service orchestration
└── README.txt                     # Documentation (this file)

---


## APIs Used

1. **GeoNames API** - `http://api.geonames.org/findNearbyPlaceNameJSON`
2. **OpenWeather API** - `http://api.openweathermap.org/data/2.5/weather`
3. **Open-Meteo Air Quality API** - `https://air-quality-api.open-meteo.com/v1/air-quality`

---

## 🏠 Target Cities

- Mérida, Yucatán
- Ciudad del Carmen, Campeche
- Mexico City, CDMX
- Monterrey, Nuevo León
- Hermosillo, Sonora

---

## ⚙️ How to Run

1. Clone the repository:
   git clone https://github.com/your-repo/etl-joseangel.git

2. The API keys are loaded from the `.env` file.

3. Start services:
   docker-compose up --build -d

4. Initialize Airflow (first time only):
   docker-compose exec airflow-webserver airflow db init

---

## 🧲 MongoDB Collections

- raw_geonames
- raw_air_quality
- raw_weather
- processed_environmental

---

## 📊 Dashboard Features

- Map of Mexico with city markers
- Hourly temperature trends
- Pollution indicators
- Alert messages for heat or pollution

---

## ⏱️ ETL Execution Logic

[Ingest GeoNames] → [Ingest OpenWeather] → [Ingest Air Quality] → [Transform Data] → [Load to MongoDB]

---

## 📊 Future Improvements

- Add more cities or countries
- Historical trends
- Email alerts
- More environmental APIs

---

## 📜 Author

José Ángel Pech Xool
ETL Project – Universidad Politécnica de Yucatán
July 2025
