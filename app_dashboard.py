import streamlit as st
import auth_utils
import config

# CONFIGURACIÓN GENERAL
# Esta configuración aplica para todo el dashboard
st.set_page_config(
    page_title="Dashboard Delitos CDMX",
    layout="wide"
)

# Inicializar sesión
auth_utils.inicializar_sesion()

# Si no está autenticado, mostrar página de login
if not st.session_state.authenticated:
    auth_utils.pagina_login(config.USUARIOS)
    st.stop()

# Usuario autenticado - definir páginas según tipo de usuario
# Páginas disponibles para todos los usuarios autenticados
pagina_analisis = st.Page(
    "pages/1_Analisis_Inicial.py",
    title="Análisis Inicial",
    icon="📊",
    default=True
)

pagina_mapa = st.Page(
    "pages/2_Mapa.py", 
    title="Mapa Geoespacial",
    icon="🗺️"
)

# Página exclusiva para usuarios privilegiados
pagina_detallado = st.Page(
    "pages/3_Analisis_Detallado.py",
    title="Análisis Detallado",
    icon="🔍"
)

# CREACIÓN DE LA NAVEGACIÓN SEGÚN TIPO DE USUARIO
if st.session_state.user_type == "privilegiado":
    # Usuario privilegiado: acceso a todas las páginas
    pg = st.navigation({
        "📈 Análisis": [pagina_analisis, pagina_mapa, pagina_detallado]
    })
else:
    # Usuario general: acceso limitado
    pg = st.navigation({
        "📈 Análisis": [pagina_analisis, pagina_mapa]
    })

# Ejecutar la navegación
pg.run()