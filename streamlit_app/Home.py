# Esta es la página principal de la aplicación Streamlit

import streamlit as st
import pandas as pd
from streamlit_app.backend_requests import obtener_todos_propietarios, obtener_todos_animales, obtener_todas_citas, obtener_todos_veterinarios

st.set_page_config(page_title="Dashboard Clínica Veterinaria", page_icon="🏥", layout="wide")


# SISTEMA DE LOGIN SIMULADO

# Usamos session_state para recordar si el usuario ya entró
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def verificar_login():
    # Contraseña sencilla para la demo
    if st.session_state.password_input == "admin123":
        st.session_state.authenticated = True
    else:
        st.error("🚫 Contraseña incorrecta")

# Si NO está autenticado, mostramos solo el login y detenemos la app
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔐 Acceso al Sistema")
        st.markdown("Por favor, identifíquese para acceder al panel de gestión veterinaria.")
        st.text_input("Contraseña de Acceso", type="password", key="password_input", on_change=verificar_login)
        st.info("💡 Pista para el profesor: La contraseña es **admin123**")
    st.stop() # 🛑 AQUÍ SE DETIENE LA EJECUCIÓN SI NO HAY LOGIN


# 🏥 APLICACIÓN PRINCIPAL 


# Sidebar con botón de salir
with st.sidebar:
    if st.button("🔒 Cerrar Sesión"):
        st.session_state.authenticated = False
        st.rerun()

st.title("🏥 Dashboard General - Clínica Veterinaria")

# Cargamos los datos globales (Cacheado sería mejor, pero así es simple)
try:
    propietarios = obtener_todos_propietarios()
    animales = obtener_todos_animales()
    citas = obtener_todas_citas()
    veterinarios = obtener_todos_veterinarios()
except Exception as e:
    st.error(f"Error conectando con el sistema: {e}")
    st.stop()


# 🔍 BUSCADOR GLOBAL 

st.markdown("### 🔍 Búsqueda Rápida")
busqueda = st.text_input("Buscar...", placeholder="Escribe nombre, teléfono, email o nombre de mascota...")

if busqueda:
    st.info(f"Resultados para: **'{busqueda}'**")
    
    # Filtros
    props = [p for p in propietarios if busqueda.lower() in p['nombre'].lower() or busqueda in p['telefono'] or busqueda.lower() in p['email'].lower()]
    anims = [a for a in animales if busqueda.lower() in a['nombre'].lower() or busqueda.lower() in a['raza'].lower()]
    vets = [v for v in veterinarios if busqueda.lower() in v['nombre'].lower() or busqueda.lower() in v['apellidos'].lower() or busqueda.lower() in v['cargo'].lower()]

    col1, col2, col3 = st.columns(3)
    
    # 1. CLIENTES ENCONTRADOS
    with col1:
        st.markdown(f"#### 👤 Clientes ({len(props)})")
        if props:
            for p in props:
                with st.expander(f"{p['nombre']}"):
                    st.write(f"📱 **Tlf:** {p['telefono']}")
                    st.write(f"📧 **Email:** {p['email']}")
                    st.caption(f"ID: {p['id']}")
        else: st.caption("Sin resultados.")

    # 2. PACIENTES ENCONTRADOS
    with col2:
        st.markdown(f"#### 🐾 Pacientes ({len(anims)})")
        if anims:
            for a in anims:
                with st.expander(f"{a['nombre']} ({a['especie']})"):
                    st.write(f"**Raza:** {a['raza']}")
                    st.write(f"**Edad:** {a['edad']} años")
                    st.caption(f"Dueño ID: {a['propietario_id']}")
        else: st.caption("Sin resultados.")

    # 3. VETERINARIOS ENCONTRADOS
    with col3:
        st.markdown(f"#### 👨‍⚕️ Equipo ({len(vets)})")
        if vets:
            for v in vets:
                with st.expander(f"Dr. {v['nombre']} {v['apellidos']}"):
                    st.write(f"📋 **Cargo:** {v['cargo']}")
                    st.write(f"🕒 **Horario:** {v['horario']}")
                    st.write(f"📞 {v['telefono']}")
        else: st.caption("Sin resultados.")
            
    st.markdown("---")


# 📊 DASHBOARD 



st.markdown("### Resumen de Actividad en Tiempo Real")

# 2. MÉTRICAS PRINCIPALES
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="👥 Total Clientes", value=len(propietarios), delta="Activos")
with col2:
    st.metric(label="🐾 Pacientes Registrados", value=len(animales), delta=f"{len(animales)} Historiales")
with col3:
    pendientes = sum(1 for c in citas if c['estado'] == "Pendiente")
    st.metric(label="📅 Citas Pendientes", value=pendientes, delta="Atención requerida", delta_color="inverse")
with col4:
    st.metric(label="👨‍⚕️ Equipo Médico", value=len(veterinarios), delta="Disponibles")

st.markdown("---")

# 3. GRÁFICOS DE ACTIVIDAD
st.markdown("### 📊 Análisis Visual")
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Distribución de Citas por Estado")
    if citas: 
        df_citas = pd.DataFrame(citas)
        if 'estado' in df_citas.columns:
            st.bar_chart(df_citas['estado'].value_counts(), color="#FF4B4B")
        else: st.warning("Datos incompletos.")
    else: st.info("Sin datos.")

with col_right:
    st.subheader("🐶 Pacientes por Especie")
    if animales:
        df_animales = pd.DataFrame(animales)
        if 'especie' in df_animales.columns:
            st.bar_chart(df_animales['especie'].value_counts(), color="#00CC96")
        else: st.warning("Datos incompletos.")
    else: st.info("Sin datos.")

# 4. ACCESOS DIRECTOS
st.markdown("### 🚀 Accesos Directos")
c1, c2, c3 = st.columns(3)
if c1.button("Registrar Nueva Cita"):
    st.switch_page("pages/4_Citas.py")
if c2.button("Nuevo Paciente"):
    st.switch_page("pages/2_Animales.py")
if c3.button("Ver Doctores"):
    st.switch_page("pages/3_Veterinarios.py")