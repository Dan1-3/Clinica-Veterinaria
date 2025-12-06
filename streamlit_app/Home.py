# Esta es la página principal de la aplicación Streamlit

import streamlit as st
import pandas as pd
from streamlit_app.backend_requests import obtener_todos_propietarios, obtener_todos_animales, obtener_todas_citas, obtener_todos_veterinarios

st.set_page_config(page_title="Dashboard Clínica Veterinaria", page_icon="🏥", layout="wide")

st.title("🏥 Dashboard General - Clínica Veterinaria")
st.markdown("### Resumen de Actividad en Tiempo Real")

# Cargamos los datos necesarios desde el backend
try:
    propietarios = obtener_todos_propietarios()
    animales = obtener_todos_animales()
    citas = obtener_todas_citas()
    veterinarios = obtener_todos_veterinarios()
except Exception as e:
    st.error(f"Error conectando con el sistema: {e}")
    st.stop()

# 2. MÉTRICAS PRINCIPALES --> Mostramos las métricas clave en cuatro columnas
st.markdown("### 📈 Métricas Clave")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="👥 Total Clientes", value=len(propietarios), delta="Activos")

with col2:
    st.metric(label="🐾 Pacientes Registrados", value=len(animales), delta=f"{len(animales)} Historiales")

with col3:
    # Calculamos citas pendientes
    pendientes = sum(1 for c in citas if c['estado'] == "Pendiente") # Contamos las citas con estado "Pendiente"
    st.metric(label="📅 Citas Pendientes", value=pendientes, delta="Atención requerida", delta_color="inverse") # delta es un texto que indica un cambio o estado adicional

with col4:
    st.metric(label="👨‍⚕️ Equipo Médico", value=len(veterinarios), delta="Disponibles")

st.markdown("---")

# 3. GRÁFICOS DE ACTIVIDAD --> Mostramos gráficos de barras para citas y animales
st.markdown("### 📊 Análisis Visual")
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Distribución de Citas por Estado")
    if citas: 
        df_citas = pd.DataFrame(citas) # Convertimos la lista de citas a DataFrame, para facilitar el conteo de estados
        if 'estado' in df_citas.columns:
            conteo_estado = df_citas['estado'].value_counts() # Contamos cuántas citas hay por cada estado
            st.bar_chart(conteo_estado, color="#FF4B4B") # Gráfico de barras 
        else:
            st.warning("Datos de citas incompletos.")
    else:
        st.info("No hay datos de citas suficientes.")

with col_right:
    st.subheader("🐶 Pacientes por Especie")
    if animales:
        df_animales = pd.DataFrame(animales)
        if 'especie' in df_animales.columns:
            conteo_especie = df_animales['especie'].value_counts() # Contamos cuántos animales hay por especie
            st.bar_chart(conteo_especie, color="#00CC96")
        else:
            st.warning("Datos de animales incompletos.")
    else:
        st.info("No hay datos de animales.")

# 4. ACCESOS DIRECTOS --> Botones para navegar a otras páginas de manera rápida
st.markdown("### 🚀 Accesos Directos")
c1, c2, c3 = st.columns(3)
if c1.button("Registrar Nueva Cita"):
    st.switch_page("pages/4_Citas.py")
if c2.button("Nuevo Paciente"):
    st.switch_page("pages/2_Animales.py")
if c3.button("Ver Doctores"):
    st.switch_page("pages/3_Veterinarios.py")