# app_dashboard.py

import streamlit as st

# === Configuración General ===
# Esta configuración aplica para toda la app y debe ir al principio
st.set_page_config(
    page_title="Dashboard Delitos CDMX",
    page_icon="⚖️",
    layout="wide"
)

# === Definición de las Páginas ===
# Aquí defines cuales son tus archivos reales y como quieres que se llamen en el menú
# default=True hace que esta sea la página que se abre automáticamente al entrar
pagina_analisis = st.Page(
    "pages/1_Analisis_Inicial.py", 
    title="Análisis Inicial", 
    icon="📋", 
    default=True
)

pagina_mapa = st.Page(
    "pages/2_Mapa.py", 
    title="Mapa Geoespacial", 
    icon="🗺️"
)

# === Creación de la Navegación ===
# Aquí agrupamos las páginas, el "archivo madre" no se incluye a sí mismo en la lista
pg = st.navigation({
    "Menú Principal": [pagina_analisis, pagina_mapa]
})

# === Ejecución ===
# Esto es lo que hace que se muestre el contenido de la página seleccionada

pg.run()
