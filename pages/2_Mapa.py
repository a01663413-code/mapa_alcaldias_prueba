# pages/2_Mapa.py
import streamlit as st
from streamlit_folium import st_folium
import data_loader
import map_utils
import plot_utils

# Configuración de la página
st.set_page_config(
    page_title="Mapa - Dashboard Delitos CDMX",
    page_icon="🗺️",
    layout="wide"
)

# Cargar datos
URL_GEOJSON_ALCALDIAS = "https://datos.cdmx.gob.mx/dataset/alcaldias/resource/8648431b-4f34-4f1a-a4b1-19142f944300/download/limite-de-las-alcaldias.json"
delegaciones = map_utils.load_geojson(URL_GEOJSON_ALCALDIAS, local_backup="limite-de-las-alcaldias.json")
data = data_loader.load_data("df_streamlit.csv")

if data.empty:
    st.error("No se pudieron cargar los datos.")
    st.stop()

# === Contenido de la página ===
st.title("🚨 Dashboard de Incidentes Delictivos – CDMX")
st.subheader("🗺️ Mapa Interactivo")

# === Sidebar de Filtros ===
st.sidebar.header("⚙️ Filtros Principales")

alcaldia = st.sidebar.selectbox(
    "Selecciona Alcaldía:",
    ["TODAS"] + sorted(data["alcaldia_hecho"].dropna().unique())
)

categoria = st.sidebar.selectbox(
    "Selecciona Categoría:",
    ["TODAS"] + sorted(data["CATEGORIA"].dropna().unique())
)

# --- Configuración del Mapa ---
st.sidebar.header("🗺️ Configuración del Mapa")
with st.sidebar.form(key="map_config_form"):
    tipo_mapa = st.multiselect(
        "Capas del Mapa:",
        ["Puntos", "Heatmap"],
        default=["Heatmap"]
    )
    
    opciones_muestreo = {
        "20% de los puntos": 0.2,
        "40% de los puntos": 0.4,
        "60% de los puntos": 0.6,
        "80% de los puntos": 0.8,
        "100% (Todos)": 1.0
    }
    
    seleccion_muestreo_texto = st.selectbox(
        "Muestreo de puntos (para rendimiento):",
        options=opciones_muestreo.keys(),
        index=len(opciones_muestreo) - 1
    )
    
    porcentaje_seleccionado = opciones_muestreo[seleccion_muestreo_texto]
    map_submit_button = st.form_submit_button(label="Aplicar Config. Mapa")

# === Filtrado de Datos ===
df_filtrado = data.copy()

if alcaldia != "TODAS":
    df_filtrado = df_filtrado[df_filtrado["alcaldia_hecho"] == alcaldia]
if categoria != "TODAS":
    df_filtrado = df_filtrado[df_filtrado["CATEGORIA"] == categoria]

if df_filtrado.empty:
    st.warning("No se encontraron registros con los filtros seleccionados.")

# === KPIs ===
st.subheader("Resumen de Incidentes (con filtros aplicados)")
kpi1, kpi2, kpi3 = st.columns(3)

total_delitos = df_filtrado.shape[0]
total_violentos = df_filtrado[df_filtrado['Violento'] == 'Violento'].shape[0]
ratio_violencia = (total_violentos / total_delitos) if total_delitos > 0 else 0

kpi1.metric("Total de Delitos", f"{total_delitos:,}")
kpi2.metric("Delitos Violentos", f"{total_violentos:,}")
kpi3.metric("Proporción Violenta", f"{ratio_violencia:.1%}")
st.markdown("---")

# === Mapa y Gráfica (2 Columnas) ===
col1, col2 = st.columns((6, 4))

with col1:
    st.subheader("Mapa de Incidencia")
    
    total_registros_filtrados = len(df_filtrado)
    num_points_calculado = int(total_registros_filtrados * porcentaje_seleccionado)
    num_points_a_usar = min(total_registros_filtrados, num_points_calculado)

    if num_points_a_usar < total_registros_filtrados:
        df_mapa = df_filtrado.sample(n=num_points_a_usar)
        st.info(f"Mostrando {num_points_a_usar} puntos ({seleccion_muestreo_texto})")
    else:
        df_mapa = df_filtrado.copy()
    
    m = map_utils.render_folium_map(
        df_mapa,
        delegaciones,
        show_points=("Puntos" in tipo_mapa),
        show_heatmap=("Heatmap" in tipo_mapa)
    )
    st_folium(m, height=450, use_container_width=True) 

with col2:
    st.subheader("Delitos por Alcaldía")
    chart_alcaldia = plot_utils.plot_delitos_por_alcaldia(df_filtrado)
    st.altair_chart(chart_alcaldia, use_container_width=True)

# === Mostrar datos crudos (filtrados) ===
if st.sidebar.checkbox("Mostrar datos crudos (filtrados)"):
    st.markdown("---")
    st.subheader("Datos Filtrados")
    st.dataframe(df_filtrado.head(100))
