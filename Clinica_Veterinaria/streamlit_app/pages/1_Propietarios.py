import streamlit as st
import pandas as pd
# Importamos las funciones de conexión
from streamlit_app.backend_requests import get_all_propietarios, create_propietario

st.title("👥 Gestión de Propietarios")
st.markdown("---")

# --- 1. FORMULARIO DE REGISTRO (POST) ---
with st.form("form_nuevo_propietario"):
    st.header("Registrar Nuevo Dueño")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input("Nombre Completo")
        email = st.text_input("Correo Electrónico")
    
    with col2:
        telefono = st.text_input("Teléfono")
        direccion = st.text_input("Dirección")
    
    submitted = st.form_submit_button("Guardar Propietario")
    
    if submitted:
        # Preparamos los datos para enviar al Backend
        nuevo_prop = {
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "direccion": direccion
        }
        
        # Enviamos la petición
        resultado = create_propietario(nuevo_prop)
        
        if resultado:
            st.success(f"Propietario '{nombre}' registrado con éxito (ID: {resultado['id']})")
            st.rerun() # Recargamos para ver el cambio en la tabla

st.markdown("---")

# --- 2. LISTADO DE PROPIETARIOS (GET) ---
st.subheader("Directorio de Clientes")

datos = get_all_propietarios()

if datos:
    df = pd.DataFrame(datos)
    # Mostramos la tabla ocupando todo el ancho
    st.dataframe(df, use_container_width=True)
else:
    st.info("No hay propietarios registrados todavía.")