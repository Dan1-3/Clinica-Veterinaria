import streamlit as st
import pandas as pd
from streamlit_app.backend_requests import obtener_todos_veterinarios, crear_veterinario


#  BLOQUEO DE SEGURIDAD

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Acceso denegado. Por favor, inicia sesión en la página principal.")
    st.stop()





st.title("👨‍⚕️ Gestión de Veterinarios")
tab_lista, tab_nuevo = st.tabs(["📋 Plantilla", "➕ Contratar"])

# Lista de veterinarios: aqui mostramos todos los veterinarios
with tab_lista:
    datos = obtener_todos_veterinarios()
    if datos:
        st.dataframe(pd.DataFrame(datos), use_container_width=True) # Mostramos la tabla usando todo el ancho del contenedor
        #pd.Dataframe(datos) convierte la lista de diccionarios en tabla, para mejor visualización
    else:
        st.info("No hay veterinarios.")

# Formulario para crear un nuevo veterinario
with tab_nuevo:
    with st.form("form_vet"):
        c1, c2 = st.columns(2)
        n = c1.text_input("Nombre")
        a = c2.text_input("Apellidos")
        c = c1.text_input("Correo")
        t = c2.text_input("Teléfono")
        h = c1.selectbox("Horario", ["Mañana", "Tarde", "Noche"])
        car = c2.text_input("Cargo")
        
        if st.form_submit_button("Registrar"):
            datos = {"nombre": n, "apellidos": a, "correo": c, "telefono": t, "horario": h, "cargo": car}
            if crear_veterinario(datos):
                st.success("Veterinario registrado"); st.rerun()