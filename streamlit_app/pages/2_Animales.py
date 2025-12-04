# Aquí se creará la página de Streamlit para mostrar y gestionar los animales.

import streamlit as st
import pandas as pd
from streamlit_app.backend_requests import get_all_animales, create_animal, get_all_propietarios

st.title("🐾 Gestión de Pacientes (Animales)")
st.markdown("---")

# 1. OBTENER PROPIETARIOS PARA EL DESPLEGABLE
lista_propietarios = get_all_propietarios()

# Creamos un diccionario para usar en la caja para seleccionar: "Nombre (ID)" -> ID real
opciones_propietarios = {f"{p['nombre']} (ID: {p['id']})": p['id'] for p in lista_propietarios}

# Formulario para crear nuevo animal
with st.form("form_animal"):
    st.header("Registrar Mascota")
    
    # Si no hay propietarios, avisamos
    if not opciones_propietarios:
        st.warning("⚠️ Primero debes registrar Propietarios para poder añadir mascotas.") 
        seleccion = None
    else:
        seleccion = st.selectbox("Selecciona al Dueño:", list(opciones_propietarios.keys()))
    
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del Animal")
        especie = st.text_input("Especie (Perro, Gato...)")
    with col2:
        raza = st.text_input("Raza")
        edad = st.number_input("Edad", min_value=0, step=1)
    
    submitted = st.form_submit_button("Guardar Animal")
    
    if submitted and seleccion:
        # Recuperamos el ID real del propietario seleccionado, para enviarlo al backend
        id_dueno = opciones_propietarios[seleccion]
        
        nuevo_animal = {
            "nombre": nombre,
            "especie": especie,
            "raza": raza,
            "edad": edad,
            "propietario_id": id_dueno
        }
        
        resultado = create_animal(nuevo_animal)
        if resultado:
            st.success(f"¡{nombre} registrado correctamente!")
            st.rerun()

st.markdown("---")

# 2. TABLA DE ANIMALES EXISTENTES (GET)
st.subheader("Pacientes en la Clínica")
datos = get_all_animales()

if datos:
    df = pd.DataFrame(datos)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No hay animales registrados.")