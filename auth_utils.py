"""
Módulo de autenticación para el dashboard de Streamlit
Maneja login, sesiones y control de acceso
"""

import streamlit as st
import hashlib


def hash_password(password: str) -> str:
    """
    Convierte una contraseña en su hash SHA256
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        Hash SHA256 de la contraseña
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verificar_credenciales(username: str, password: str, usuarios: dict) -> tuple:
    """
    Verifica si las credenciales son válidas
    
    Args:
        username: Nombre de usuario
        password: Contraseña en texto plano
        usuarios: Diccionario con usuarios y sus configuraciones
        
    Returns:
        tuple: (autenticado: bool, tipo_usuario: str, nombre_usuario: str)
    """
    if username in usuarios:
        password_hash = hash_password(password)
        if usuarios[username]["password_hash"] == password_hash:
            return True, usuarios[username]["tipo"], username
    return False, None, None


def inicializar_sesion():
    """
    Inicializa las variables de sesión necesarias
    """
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_type" not in st.session_state:
        st.session_state.user_type = None
    if "username" not in st.session_state:
        st.session_state.username = None


def login(username: str, password: str, usuarios: dict) -> bool:
    """
    Realiza el proceso de login
    
    Args:
        username: Nombre de usuario
        password: Contraseña
        usuarios: Diccionario de usuarios
        
    Returns:
        bool: True si el login fue exitoso
    """
    autenticado, tipo_usuario, nombre = verificar_credenciales(username, password, usuarios)
    
    if autenticado:
        st.session_state.authenticated = True
        st.session_state.user_type = tipo_usuario
        st.session_state.username = nombre
        return True
    return False


def login_invitado():
    """
    Realiza el login como usuario invitado (sin credenciales)
    """
    st.session_state.authenticated = True
    st.session_state.user_type = "general"
    st.session_state.username = "Invitado"


def logout():
    """
    Cierra la sesión del usuario
    """
    st.session_state.authenticated = False
    st.session_state.user_type = None
    st.session_state.username = None


def requiere_autenticacion(user_types: list = None):
    """
    Verifica que el usuario esté autenticado y tenga el tipo correcto
    Redirige a la página de login si no está autenticado
    
    Args:
        user_types: Lista de tipos de usuario permitidos (None = todos los autenticados)
    """
    if not st.session_state.get("authenticated", False):
        st.warning("⚠️ Debes iniciar sesión para acceder a esta página.")
        st.stop()
    
    if user_types and st.session_state.get("user_type") not in user_types:
        st.error("🚫 No tienes permisos para acceder a esta página.")
        st.stop()


def mostrar_info_usuario_sidebar():
    """
    Muestra información del usuario y botón de logout al final del sidebar
    """
    # Usar un contenedor al final para el botón de cerrar sesión
    # Esto asegura que siempre esté al final, después de los filtros
    pass  # El contenido se agregará después de la navegación


def renderizar_logout_sidebar():
    """
    Renderiza el botón de logout al final del sidebar (llamar al final de cada página)
    """
    # Spacer para empujar el contenido al final
    st.sidebar.markdown("")
    st.sidebar.markdown("---")
    
    tipo_emoji = "🔑" if st.session_state.user_type == "privilegiado" else "👥"
    tipo_texto = "Privilegiado" if st.session_state.user_type == "privilegiado" else "General"
    
    st.sidebar.info(f"{tipo_emoji} **{st.session_state.username}**\n\nTipo: {tipo_texto}")
    
    if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
        logout()
        st.rerun()


def pagina_login(usuarios: dict):
    """
    Renderiza la página de login
    
    Args:
        usuarios: Diccionario con las credenciales de usuarios
    """
    # Ocultar sidebar completamente
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Centrar el contenido
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            """
            <div style="text-align: center; padding: 2rem 0;">
                <h1 style="color: #9F2241;">Dashboard Delitos CDMX</h1>
                <p style="font-size: 1.2rem; color: #666;">Sistema de Análisis de Criminalidad</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        
        # Tabs para login y acceso invitado
        tab1, tab2 = st.tabs(["🔑 Login Usuario", "👥 Acceso Invitado"])
        
        with tab1:
            st.markdown("### Iniciar Sesión")
            
            with st.form("login_form"):
                username = st.text_input("Usuario", placeholder="Ingresa tu usuario")
                password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")
                submit = st.form_submit_button("Iniciar Sesión", use_container_width=True)
                
                if submit:
                    if username and password:
                        if login(username, password, usuarios):
                            st.success("✅ Login exitoso! Redirigiendo...")
                            st.rerun()
                        else:
                            st.error("❌ Usuario o contraseña incorrectos")
                    else:
                        st.warning("⚠️ Por favor completa todos los campos")
        
        with tab2:
            st.markdown("### Acceso como Invitado")
            st.info("Accede sin credenciales con permisos limitados")
            
            if st.button("Acceder como Invitado", use_container_width=True, type="primary"):
                login_invitado()
                st.success("✅ Acceso como invitado concedido! Redirigiendo...")
                st.rerun()
        
        st.markdown("---")
        
        # Información de credenciales de prueba
        with st.expander("ℹ️ Credenciales de prueba"):
            st.markdown("""
            **Usuario Privilegiado:**
            - Usuario: `admin`
            - Contraseña: `admin123`
            """)
