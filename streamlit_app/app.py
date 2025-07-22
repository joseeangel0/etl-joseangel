import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

# Configuración de página
st.set_page_config(page_title="🌎 Dashboard Ambiental", layout="wide")

# Conexión Mongo
client = MongoClient("host.docker.internal", 27018)
db = client["clima_db"]
docs = list(db["ciudades_clima"].find())
df = pd.json_normalize(docs)

# Limpiar ID y convertir fecha
df.drop(columns=["_id"], inplace=True)
df["ingested_at"] = pd.to_datetime(df["ingested_at"])

# Título principal
st.title("📍 Perfil Ambiental por Ciudad")
st.markdown("Visualización de clima, calidad del aire y condiciones ambientales por ciudad en México.")

# Selector de ciudad
ciudades = df["city"].unique().tolist()
ciudad = st.selectbox("Selecciona una ciudad", ciudades)

df_ciudad = df[df["city"] == ciudad].copy()

# Línea de tendencia de temperatura por hora
st.subheader("📈 Tendencia de Temperatura por Hora")

df_trend = (
    df[df["city"] == ciudad]
    .sort_values("ingested_at")
    .loc[:, ["ingested_at", "temperature"]]
)

if not df_trend.empty:
    fig_trend = px.line(
        df_trend,
        x="ingested_at",
        y="temperature",
        markers=True,
        title=f"Evolución Horaria de Temperatura en {ciudad}",
        labels={"ingested_at": "Hora", "temperature": "°C"},
    )
    st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.info("Aún no hay datos históricos suficientes para esta ciudad.")

# Métricas principales
col1, col2, col3 = st.columns(3)
col1.metric("🌡️ Temperatura", f"{df_ciudad['temperature'].values[0]} °C")
col2.metric("💧 Humedad", f"{df_ciudad['humidity'].values[0]} %")
col3.metric("🌧️ Precipitación", f"{df_ciudad['precipitation_mm'].values[0]} mm")

# Estado del clima
st.subheader("🌤️ Condición del Clima")
st.info(f"Condición: **{df_ciudad['weather_condition'].values[0]}**")

# Contaminantes
st.subheader("🧪 Contaminantes del Aire")

# 💬 Explicación sencilla para el usuario
st.markdown("""
💨 Este gráfico muestra los niveles de tres contaminantes comunes en el aire:

- **PM2.5** y **PM10**: partículas finas que pueden penetrar profundamente en los pulmones.
- **Ozono (O₃)**: gas que a nivel del suelo puede causar problemas respiratorios.

Los valores están expresados en **microgramos por metro cúbico (µg/m³)** para que puedan compararse directamente.
""")

# 🔍 Extraer datos desde df_ciudad
pm25 = df_ciudad["air_quality.pm2_5"].values[0]
pm10 = df_ciudad["air_quality.pm10"].values[0]
ozono_ppb = df_ciudad["air_quality.ozone"].values[0]

# 🔁 Conversión de ozono de ppb a µg/m³ (aproximado)
ozono_ugm3 = ozono_ppb * 2

# 📊 Crear DataFrame para graficar
pollutants = {
    "PM2.5 (µg/m³)": pm25,
    "PM10 (µg/m³)": pm10,
    "Ozono (µg/m³ aprox)": ozono_ugm3
}
pollutants_df = pd.DataFrame(list(pollutants.items()), columns=["Contaminante", "Valor"])

# 📈 Gráfico de barras
fig = px.bar(pollutants_df, x="Contaminante", y="Valor", color="Contaminante", title="Niveles de Contaminación")
st.plotly_chart(fig, use_container_width=True)

# 📝 Nota sobre la conversión
st.caption("⚠️ El valor de Ozono ha sido convertido de ppb a µg/m³ de forma aproximada (1 ppb ≈ 2 µg/m³).")

# 🚦 Evaluación textual simple
st.markdown("### 🧭 Evaluación rápida de calidad del aire:")

# Límites OMS
limites = {
    "PM2.5": 15,
    "PM10": 45,
    "Ozono": 100
}

# Evaluación
if pm25 > limites["PM2.5"]:
    st.warning(f"🔴 PM2.5 está por encima del límite saludable (15 µg/m³). Valor actual: {pm25:.1f}")
else:
    st.success(f"🟢 PM2.5 está dentro del rango saludable. Valor actual: {pm25:.1f}")

if pm10 > limites["PM10"]:
    st.warning(f"🟠 PM10 supera el límite recomendado (45 µg/m³). Valor actual: {pm10:.1f}")
else:
    st.success(f"🟢 PM10 está dentro del rango saludable. Valor actual: {pm10:.1f}")

if ozono_ugm3 > limites["Ozono"]:
    st.error(f"🔴 Ozono está por encima del límite (100 µg/m³). Valor actual: {ozono_ugm3:.1f}")
else:
    st.success(f"🟢 Ozono está en un nivel aceptable. Valor actual: {ozono_ugm3:.1f}")


# Alertas (si hay)
st.subheader("⚠️ Alertas")
alertas = df_ciudad["alerts"].values[0]
if alertas:
    for alerta in alertas:
        st.error(f"🔔 {alerta}")
else:
    st.success("✅ No hay alertas activas para esta ciudad.")

#MAPA DE LAS CIUDADES
st.subheader("🗺️ Mapa de todas las ciudades registradas")
df_map = df.dropna(subset=["latitude", "longitude"])
# Asegurarse de que lat/lon sean numéricos
df_map["latitude"] = pd.to_numeric(df_map["latitude"], errors="coerce")
df_map["longitude"] = pd.to_numeric(df_map["longitude"], errors="coerce")
df_map = df_map.dropna(subset=["latitude", "longitude"])

if not df_map.empty:
    st.map(df_map[["latitude", "longitude"]])
else:
    st.warning("No hay coordenadas válidas para mostrar el mapa.")

# Tabla detallada
st.subheader("📋 Datos completos")
st.dataframe(df_ciudad.T.rename(columns={df_ciudad.index[0]: "Valor"}))





