# pages/2_Mapa.py
import streamlit as st
from streamlit_folium import st_folium
import data_loader
import map_utils
import plot_utils

# Configuración de la página
st.set_page_config(
    page_title="Mapa Interactivo - Dashboard Delitos CDMX",
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
    ["TODAS"] + sorted(data["delito"].dropna().unique())
)

tipo_mapa = st.sidebar.radio(
    "Tipo de Visualización:",
    ["Puntos", "Heatmap"]
)

# === Filtrar Datos ===
data_filtered = data.copy()

if alcaldia != "TODAS":
    data_filtered = data_filtered[data_filtered["alcaldia_hecho"] == alcaldia]

if categoria != "TODAS":
    data_filtered = data_filtered[data_filtered["delito"] == categoria]

# === KPIs ===
st.markdown("### 📊 Indicadores Clave")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Incidentes", f"{len(data_filtered):,}")

with col2:
    if len(data_filtered) > 0:
        alcaldia_top = data_filtered["alcaldia_hecho"].value_counts().index[0]
        st.metric("Alcaldía con Más Incidentes", alcaldia_top)
    else:
        st.metric("Alcaldía con Más Incidentes", "N/A")

with col3:
    if len(data_filtered) > 0:
        delito_top = data_filtered["delito"].value_counts().index[0]
        st.metric("Delito Más Común", delito_top[:20] + "...")
    else:
        st.metric("Delito Más Común", "N/A")

with col4:
    if 'Violento' in data_filtered.columns:
        pct_violento = (data_filtered['Violento'] == 'Violento').mean() * 100
        st.metric("% Violentos", f"{pct_violento:.1f}%")
    else:
        st.metric("% Violentos", "N/A")

st.markdown("---")

# === Mapa ===
st.markdown("### 🗺️ Mapa de Incidencias")

if len(data_filtered) == 0:
    st.warning("⚠️ No hay datos para mostrar con los filtros seleccionados.")
else:
    if tipo_mapa == "Puntos":
        mapa = map_utils.create_points_map(data_filtered, delegaciones)
    else:
        mapa = map_utils.create_heatmap(data_filtered, delegaciones)
    
    st_folium(mapa, width=1200, height=600)

st.markdown("---")

# === Gráficas por Alcaldía ===
st.markdown("### 📊 Análisis por Alcaldía")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("##### Delitos por Alcaldía")
    chart_alcaldia = plot_utils.plot_delitos_por_alcaldia(data_filtered)
    st.altair_chart(chart_alcaldia, use_container_width=True)

with col_right:
    st.markdown("##### Top 10 Delitos")
    chart_top_delitos = plot_utils.plot_top_delitos(data_filtered, top_n=10)
    st.altair_chart(chart_top_delitos, use_container_width=True)

st.markdown("---")

# === Información Adicional ===
with st.expander("ℹ️ Información sobre los Datos"):
    st.markdown("""
    **Fuente de Datos:** Datos abiertos de la Ciudad de México
    
    **Filtros Aplicados:**
    - Alcaldía: `{}`
    - Categoría: `{}`
    - Tipo de Mapa: `{}`
    
    **Total de registros filtrados:** {:,}
    """.format(alcaldia, categoria, tipo_mapa, len(data_filtered)))
