import streamlit as st
import pandas as pd
from datetime import datetime, time
import requests

# Configuración de página
st.set_page_config(page_title="Gestión de Citas", page_icon="📅")
st.title("Gestión de Citas")
st.markdown("---")

# URL del Backend
FASTAPI_URL = "http://127.0.0.1:8000"

# --- FUNCIONES DE CARGA ---
def get_data(endpoint):
    try:
        r = requests.get(f"{FASTAPI_URL}/{endpoint}/")
        return r.json() if r.status_code == 200 else []
    except: return []

# 1. Cargar datos para los selectores
animales = get_data("animales")
veterinarios = get_data("veterinarios")

# Crear diccionarios para mapear "Nombre en pantalla" -> "ID real"
mapa_animales = {}
if animales:
    # Mostramos: Nombre (Especie)
    mapa_animales = {f"{a['nombre']} ({a['especie']})": a for a in animales}

mapa_vets = {}
if veterinarios:
    # Mostramos: Nombre Apellido (Cargo)
    mapa_vets = {f"{v['nombre']} {v['apellidos']} ({v['cargo']})": v['id'] for v in veterinarios}

# --- FORMULARIO ---
with st.form("form_cita"):
    st.subheader("Agendar Nueva Cita")

    col1, col2 = st.columns(2)
    with col1:
        # Selector de Animal
        if not mapa_animales:
            st.warning("No hay animales registrados.")
            sel_animal = None
        else:
            sel_animal = st.selectbox("Paciente:", list(mapa_animales.keys()))
            
    with col2:
        # Selector de Veterinario
        if not mapa_vets:
            st.warning("No hay veterinarios registrados.")
            sel_vet = None
        else:
            sel_vet = st.selectbox("Veterinario:", list(mapa_vets.keys()))

    col3, col4 = st.columns(2)
    with col3:
        fecha = st.date_input("Fecha", min_value=datetime.today())
    with col4:
        hora = st.time_input("Hora", value=time(9,0))

    motivo = st.text_area("Motivo de la consulta")
    
    submitted = st.form_submit_button("Guardar Cita")

    if submitted and sel_animal and sel_vet:
        # Recuperamos los objetos/IDs reales
        animal_obj = mapa_animales[sel_animal]
        vet_id = mapa_vets[sel_vet]
        
        # Construimos la fecha ISO
        fecha_iso = datetime.combine(fecha, hora).isoformat()

        payload = {
            "fecha_hora": fecha_iso,
            "motivo": motivo,
            "estado": "Pendiente",
            "animal_id": animal_obj['id'],
            "propietario_id": animal_obj['propietario_id'], # Dato automático
            "veterinario_id": vet_id
        }
        
        try:
            res = requests.post(f"{FASTAPI_URL}/citas/", json=payload)
            if res.status_code == 200:
                st.success("✅ Cita agendada correctamente")
                st.rerun() # Recarga la página
            else:
                st.error(f"Error del servidor: {res.text}")
        except Exception as e:
            st.error(f"No se pudo conectar: {e}")

st.markdown("---")

# --- LISTADO ---
st.subheader("Agenda Actual")
citas = get_data("citas")
if citas:
    df = pd.DataFrame(citas)
    # Seleccionamos columnas clave para mostrar
    st.dataframe(df[["id", "fecha_hora", "motivo", "estado", "animal_id", "veterinario_id"]], use_container_width=True)
else:
    st.info("No hay citas programadas.")