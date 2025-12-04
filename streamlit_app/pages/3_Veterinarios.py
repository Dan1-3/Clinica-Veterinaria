import streamlit as st
import pandas as pd
from streamlit_app.backend_requests import get_all_veterinarios, create_veterinario

st.title("👨‍⚕️ Gestión de Veterinarios")
st.markdown("---")

# 1. FORMULARIO DE REGISTRO (POST)
with st.form("form_vet"):
    st.header("Registrar Nuevo Veterinario")
    
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre")
        correo = st.text_input("Correo Electrónico")
        horario = st.selectbox("Horario", ["Mañana", "Tarde", "Noche", "Rotativo"])
    with col2:
        apellidos = st.text_input("Apellidos")
        telefono = st.text_input("Teléfono")
        cargo = st.text_input("Cargo (Ej: Cirujano, Auxiliar...)")

    submitted = st.form_submit_button("Registrar Veterinario")
    
    if submitted:
        nuevo_vet = {
            "nombre": nombre,
            "apellidos": apellidos,
            "correo": correo,
            "telefono": telefono,
            "horario": horario,
            "cargo": cargo
        }
        resultado = create_veterinario(nuevo_vet)
        if resultado:
            st.success(f"Veterinario {nombre} registrado con éxito.")
            st.rerun()

st.markdown("---")

# 2. TABLA DE VETERINARIOS EXISTENTES (GET)
st.subheader("Plantilla Actual")
datos = get_all_veterinarios()
if datos:
    st.dataframe(pd.DataFrame(datos), use_container_width=True)
else:
    st.info("No hay veterinarios registrados.")