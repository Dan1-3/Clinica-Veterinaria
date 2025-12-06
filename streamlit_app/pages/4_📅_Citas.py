import streamlit as st
import pandas as pd
from datetime import datetime, time
import requests

# Configuración de la página, incluyendo layout wide (pantalla ancha)
st.set_page_config(page_title="Agenda", page_icon="📅", layout="wide")
FASTAPI_URL = "http://127.0.0.1:8000" # URL del backend FastAPI

# Función para obtener datos genéricos desde el backend, usada para citas y veterinarios
def get_data(endpoint):
    try:
        r = requests.get(f"{FASTAPI_URL}/{endpoint}/")
        return r.json() if r.status_code == 200 else []
    except: return []

st.title("📅 Agenda de Citas")

# Añadimos pestañas (tabs) para ver la agenda o crear una nueva cita 
tab_agenda, tab_nueva = st.tabs(["📆 Ver Agenda", "➕ Nueva Cita"])

# Pestaña 1: VER AGENDA--> Mostramos todas las citas en una tabla con filtros
with tab_agenda:
    citas = get_data("citas")
    veterinarios = get_data("veterinarios")
    
    if citas and veterinarios: # Si hay citas y veterinarios, mostramos la tabla con filtros
        df_citas = pd.DataFrame(citas)
        
        # Convertir fecha a objeto datetime para poder filtrar
        df_citas['fecha_hora'] = pd.to_datetime(df_citas['fecha_hora'])
        
        # Filtros para la agenda, arriba de la tabla
        st.markdown("### 🔍 Filtros de Agenda")
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            # Filtro por Veterinario
            vets_dict = {v['id']: v['nombre'] for v in veterinarios} # Mapa ID -> Nombre
            lista_vets = ["Todos"] + list(vets_dict.values()) # Lista de nombres con "Todos" al inicio
            filtro_vet = st.selectbox("Filtrar por Veterinario:", lista_vets) # Selector desplegable
            
        with col_f2:
            # Filtro por Estado
            filtro_estado = st.selectbox("Estado:", ["Todos", "Pendiente", "Realizada", "Cancelada"])

        # Aplicar filtros, si no es "Todos", filtramos el DataFrame. Con todos no hacemos nada porque ya están todos mostrados
        if filtro_vet != "Todos":
            # Buscamos el ID del nombre seleccionado
            id_vet_sel = [k for k, v in vets_dict.items() if v == filtro_vet][0] # Obtenemos el ID del veterinario seleccionado
            df_citas = df_citas[df_citas['veterinario_id'] == id_vet_sel] # Filtramos por ID
            
        if filtro_estado != "Todos":
            df_citas = df_citas[df_citas['estado'] == filtro_estado] # Filtramos por estado

        # MOSTRAR LA TABLA CON CONFIGURACIÓN DE COLUMNAS
        st.dataframe(
            df_citas,
            column_config={
                "fecha_hora": st.column_config.DatetimeColumn("Fecha y Hora", format="D MMM YYYY, h:mm a"),
                "estado": st.column_config.TextColumn("Estado"),
                "motivo": "Motivo Visita"
            },
            use_container_width=True,
            hide_index=True # Ocultamos la columna de índice, que no aporta nada al usuario
        )
        
        # Caption con número de citas mostradas, para información del usuario
        st.caption(f"Mostrando {len(df_citas)} citas coincidentes.")
        
    else: # No hay citas o no hay veterinarios
        st.info("No hay citas programadas o no hay veterinarios registrados.")

# Pestaña 2: NUEVA CITA --> Formulario para crear una nueva cita
with tab_nueva: # Si no hay veterinarios o animales, no podemos crear citas
    animales = get_data("animales")
    
    # Explicacion de estas lineas: Si hay animales, creamos un diccionario donde la clave es "Nombre (Especie)" y el valor es el objeto animal completo. 
    # Si no hay animales, el diccionario queda vacío.
    mapa_animales = {f"{a['nombre']} ({a['especie']})": a for a in animales} if animales else {} # Mapa Nombre -> Objeto animal
    mapa_vets = {f"{v['nombre']} {v['apellidos']}": v['id'] for v in veterinarios} if veterinarios else {} # Mapa Nombre -> ID veterinario

    # Si no hay animales o veterinarios, mostramos advertencia
    with st.form("form_cita_nueva"):
        c1, c2 = st.columns(2)
        sel_animal = c1.selectbox("Paciente", list(mapa_animales.keys())) if mapa_animales else None # Selector de animal
        sel_vet = c2.selectbox("Veterinario", list(mapa_vets.keys())) if mapa_vets else None # Selector de veterinario
        
        #  seleccionar fecha y hora, motivo
        c3, c4 = st.columns(2) 
        fecha = c3.date_input("Fecha", min_value=datetime.today())
        hora = c4.time_input("Hora", value=time(9,0))
        motivo = st.text_area("Motivo")
        
        # Botón para agendar la cita, si no hay animales o veterinarios, el botón estará deshabilitado
        if st.form_submit_button("Agendar"):
            if sel_animal and sel_vet:
                animal_obj = mapa_animales[sel_animal]
                payload = { # Diccionario con los datos de la nueva cita
                    "fecha_hora": datetime.combine(fecha, hora).isoformat(),
                    "motivo": motivo,
                    "estado": "Pendiente",
                    "animal_id": animal_obj['id'],
                    "propietario_id": animal_obj['propietario_id'],
                    "veterinario_id": mapa_vets[sel_vet]
                }
                try: # Enviamos la petición POST al backend para crear la cita
                    r = requests.post(f"{FASTAPI_URL}/citas/", json=payload)
                    if r.status_code == 200:
                        st.success("Cita agendada")
                        st.rerun()
                    else: st.error(r.text)
                except Exception as e: st.error(f"Error: {e}")