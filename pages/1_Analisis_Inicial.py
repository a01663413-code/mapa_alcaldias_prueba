# pages/1_Analisis_Inicial.py
import streamlit as st
import data_loader
import plot_utils

# Configuración de la página
st.set_page_config(
    page_title="Análisis Inicial - Dashboard Delitos CDMX",
    page_icon="📊",
    layout="wide"
)

# Cargar datos
data = data_loader.load_data("df_streamlit.csv") 
data_completo = data_loader.load_data("hour_crimes_cleaned.csv")

if data.empty:
    st.error("No se pudieron cargar los datos.")
    st.stop()

# === Contenido de la página ===
st.title("🚨 Dashboard de Incidentes Delictivos – CDMX")
st.subheader("📊 Análisis Inicial")

# === Filtro de Año ===
st.sidebar.header("⚙️ Filtros")
years_available = sorted(data_completo['anio_hecho_N'].dropna().unique().astype(int))
selected_years = st.sidebar.multiselect(
    "Selecciona Año(s):",
    options=years_available,
    default=years_available,
    help="Selecciona uno o más años para filtrar los gráficos"
)

# Filtrar datos según año seleccionado
if selected_years:
    data_completo_filtered = data_completo[data_completo['anio_hecho_N'].isin(selected_years)]
    st.markdown(f"**Años seleccionados:** {', '.join(map(str, selected_years))}")
else:
    data_completo_filtered = data_completo
    st.markdown("**Mostrando todos los años**")

# --- Fila 1: Gráficas (2 Columnas) ---
col3, col4 = st.columns(2)

with col3:
    st.markdown("##### Gráfico 2: Volumen Total y Fracción Violenta")
    chart2 = plot_utils.plot_volumen_total_violencia_hora(data_completo_filtered)
    st.altair_chart(chart2, use_container_width=True)
    
with col4:
    st.markdown("##### Proporción de Violencia (General)")
    chart_donut = plot_utils.plot_proporcion_violencia(data)
    st.altair_chart(chart_donut, use_container_width=True)

st.markdown("---")

# --- Fila 2: Gráficas (2 Columnas) ---
col5, col6 = st.columns(2)

with col5:
    st.markdown("##### Gráfico 1: Frecuencia de Crímenes Violentos")
    chart1 = plot_utils.plot_crimenes_violentos_por_hora(data_completo_filtered)
    st.altair_chart(chart1, use_container_width=True)
    
with col6:
    st.markdown("##### Gráfico 3: Porcentaje de Crímenes Violentos")
    chart3 = plot_utils.plot_ratio_violencia_hora(data_completo_filtered)
    st.altair_chart(chart3, use_container_width=True)
    
st.markdown("---")

# --- Fila 3: Gráficas (2 Columnas) ---
col7, col8 = st.columns(2)

with col7:
    st.markdown("##### Heatmap de Incidencia (Día vs. Hora)")
    chart_heatmap = plot_utils.plot_heatmap_dia_hora(data_completo_filtered)
    st.altair_chart(chart_heatmap, use_container_width=True)

with col8:
    st.markdown("##### Gráfico 4/5: Proporción Violenta (Polar)")
    chart_polar = plot_utils.plot_polar_violencia_hora(data_completo_filtered)
    st.altair_chart(chart_polar, use_container_width=True)
