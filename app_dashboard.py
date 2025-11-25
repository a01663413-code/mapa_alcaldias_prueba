import streamlit as st

# CONFIGURACIÓN GENERAL
# Esta configuración aplica para todo el dashboard
st.set_page_config(
    page_title="Dashboard Delitos CDMX",
    page_icon="⚖️",
    layout="wide"
)

# DEFINICIÓN DE LAS PÁGINAS
pagina_analisis = st.Page(
    "pages/1_Analisis_Inicial.py", # archivo que jala
    title="Dashboard Inicial",
    default=True
)

pagina_mapa = st.Page(
    "pages/2_Mapa.py", 
    title="Mapa Interactivo"
)

# CREACIÓN DE LA NAVEGACIÓN
pg = st.navigation({
    "Menú Principal": [pagina_analisis, pagina_mapa]
})

pg.run()