# Pages son las diferentes pantallas de la aplicación Streamlit, el frontend

import streamlit as st
import pandas as pd
# Importamos las nuevas funciones 
from streamlit_app.backend_requests import obtener_todos_propietarios, crear_propietario, actualizar_propietario, eliminar_propietario

st.title("👥 Gestión de Propietarios")

# Usamos 3 pestañas para organizar, una para listar, otra para crear y otra para editar/borrar
tab_lista, tab_nuevo, tab_gestion = st.tabs(["📋 Listado", "➕ Nuevo Registro", "⚙️ Editar / Borrar"])

# Pestaña 1: LISTADO
with tab_lista:
    st.header("Directorio de Clientes")
    datos = obtener_todos_propietarios() # Llamada a la función para obtener todos los propietarios
    
    if datos: # Si hay datos, los mostramos en una tabla
        st.dataframe(pd.DataFrame(datos), use_container_width=True)
    else: # Si no hay datos, mostramos un mensaje informativo
        st.info("No hay propietarios registrados todavía.")

# Pestaña 2: NUEVO REGISTRO DE PROPIETARIO
with tab_nuevo:
    st.header("Registrar Nuevo Dueño")
    with st.form("form_nuevo_propietario"): # Formulario para crear un nuevo propietario
        col1, col2 = st.columns(2) # Dividimos el formulario en dos columnas para mejor organización
        
        # En cada columna, añadimos los campos necesarios
        with col1: 
            nombre = st.text_input("Nombre Completo")
            email = st.text_input("Correo Electrónico")
        with col2:
            telefono = st.text_input("Teléfono (Empieza por 6)")
            direccion = st.text_input("Dirección")
        
        if st.form_submit_button("Guardar Propietario"):
            # Creamos el diccionario de datos, que coincide con el modelo del backend
            nuevo_prop = {
                "nombre": nombre, "email": email, 
                "telefono": telefono, "direccion": direccion
            }
            # Llamamos a la función de crear propietario para enviar los datos al backend
            resultado = crear_propietario(nuevo_prop)
            
            if resultado: # Si la creación fue exitosa, mostramos un mensaje de éxito
                st.success(f"¡Propietario '{nombre}' registrado con éxito!")
                st.rerun()

# Pestaña 3: GESTION PROPIETARIO (EDITAR / BORRAR)
with tab_gestion:
    st.header("Modificar Datos")
    
    # Necesitamos cargar los datos para elegir a quién editar
    if not datos:
        st.warning("Primero debes registrar propietarios.")
    else:
        # Creamos un selector: "Nombre (Email)" -> Objeto completo
        mapa_props = {f"{p['nombre']} ({p['email']})": p for p in datos} # Diccionario para selección de propietarios
        seleccion = st.selectbox("Selecciona un propietario:", list(mapa_props.keys())) # Selector desplegable, keys son los nombres
        
        if seleccion: # Si se ha seleccionado un propietario, mostramos su información
            prop_actual = mapa_props[seleccion]
            st.divider()
            
            # Editamos los datos del propietario seleccionado
            st.subheader(f"Editando a: {prop_actual['nombre']}")
            
            with st.form("form_editar"):
                c1, c2 = st.columns(2)
                # Cargamos los datos actuales en los campos del formulario
                new_nom = c1.text_input("Nombre", value=prop_actual['nombre'])
                new_ema = c2.text_input("Email", value=prop_actual['email'])
                new_tel = c1.text_input("Teléfono", value=prop_actual['telefono'])
                new_dir = c2.text_input("Dirección", value=prop_actual['direccion'])
                
                # Guardar cambios, pulsando el botón
                if st.form_submit_button("💾 Guardar Cambios"):
                    datos_actualizados = {
                        "nombre": new_nom, "email": new_ema, 
                        "telefono": new_tel, "direccion": new_dir
                    }
                    # Llamada a actualizar, si es exitosa, mostramos mensaje
                    if actualizar_propietario(prop_actual['id'], datos_actualizados):
                        st.success("Datos actualizados correctamente.")
                        st.rerun()
            
            # Zona de peligro: eliminar propietario, con confirmación
            st.divider()
            with st.expander("🚨 Zona de Peligro - Eliminar Propietario"):
                st.warning("Esta acción borrará al propietario y todas sus mascotas asociadas.")
                
                # Checkbox de seguridad, para confirmar eliminación
                confirmado = st.checkbox("Estoy seguro de que quiero eliminar este registro", key="check_delete_prop")
                
                # El botón solo se activa si el checkbox está marcado (disabled=not confirmado)
                if st.button("🗑️ Eliminar definitivamente", type="primary", disabled=not confirmado, key="btn_delete_prop"):
                    if eliminar_propietario(prop_actual['id']): # Llamada a la función de eliminar
                        st.success("Propietario eliminado correctamente.")
                        st.rerun() # Recargamos la página para actualizar la lista