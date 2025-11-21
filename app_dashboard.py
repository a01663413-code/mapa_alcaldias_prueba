# app_dashboard.py
# -----------------------------------------------------------------------------
# PÁGINA DE INICIO - DASHBOARD DELITOS CDMX
# 
# Ahora las páginas están en la carpeta /pages/:
# - pages/1_Analisis_Inicial.py
# - pages/2_Mapa.py
# 
# Usa el menú lateral para navegar entre páginas
# -----------------------------------------------------------------------------

import streamlit as st
import data_loader

# === Configuración de la Página ===
st.set_page_config(
    page_title="Dashboard Delitos CDMX",
    page_icon="🚨",
    layout="wide"
)

# === Cargar datos para mostrar info general ===
data = data_loader.load_data("df_streamlit.csv")

# === Página de Inicio ===
st.title("🚨 Dashboard de Incidentes Delictivos – CDMX")
st.markdown("---")

st.markdown("""
### Bienvenido al Dashboard de Análisis Delictivo

Este dashboard te permite explorar y analizar datos de incidentes delictivos en la Ciudad de México.

**Usa el menú lateral** para navegar entre las diferentes secciones:
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Análisis Inicial")
    st.markdown("""
    - Visualizaciones generales
    - Gráficos de frecuencia y volumen
    - Heatmaps temporales
    - Análisis de violencia
    
    *Ver todos los datos sin filtros*
    """)

with col2:
    st.subheader("🗺️ Mapa Interactivo")
    st.markdown("""
    - Mapa con capas (Puntos/Heatmap)
    - Filtros por alcaldía y categoría
    - KPIs dinámicos
    - Gráficos por alcaldía
    
    *Explorar con filtros personalizados*
    """)

st.markdown("---")

# === Información General ===
if not data.empty:
    st.subheader("📊 Información General del Dataset")
    
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.metric("Total de Registros", f"{len(data):,}")
    
    with col_info2:
        st.metric("Alcaldías", data["alcaldia_hecho"].nunique())
    
    with col_info3:
        if 'delito' in data.columns:
            st.metric("Tipos de Delito", data["delito"].nunique())

st.markdown("---")
st.info("👈 **Usa el menú lateral** para comenzar tu análisis")