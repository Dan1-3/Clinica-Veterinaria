# Aquí se creará la página de Streamlit para mostrar y gestionar los animales.

import streamlit as st
import pandas as pd
from streamlit_app.backend_requests import obtener_todos_animales, crear_animal, actualizar_animal, eliminar_animal, obtener_todos_propietarios, obtener_historial_animal

#  BLOQUEO DE SEGURIDAD

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Acceso denegado. Por favor, inicia sesión en la página principal.")
    st.stop()




st.title("🐾 Gestión de Pacientes")
# Definimos las pestañas para listar, crear y gestionar animales
tab_lista, tab_ficha, tab_nuevo, tab_gestion = st.tabs(["📋 Listado", "📂 Historial Médico", "➕ Nuevo Paciente", "⚙️ Editar / Borrar"])

# Tab 1: LISTADO --> Mostramos todos los animales en una tabla
with tab_lista:
    datos = obtener_todos_animales()
    if datos: # Si hay datos, los mostramos en una tabla
        df = pd.DataFrame(datos)
        st.dataframe(df, use_container_width=True) # Mostramos la tabla usando todo el ancho del contenedor
    else: 
        st.info("No hay animales registrados.")

# Tab 2: FICHA --> Mostrar el historial médico completo de un animal

with tab_ficha:
    st.header("📂 Expediente Clínico")
    st.caption("Consulta cronológica de todas las visitas y tratamientos de un paciente.")
    
    # Recargamos datos para asegurar que la lista está actualizada
    if not datos:
        st.warning("No hay pacientes registrados para consultar.")
    else:
        # Selector de paciente
        mapa_anim = {f"{a['nombre']} ({a['especie']})": a['id'] for a in datos}
        seleccion = st.selectbox("Buscar Paciente:", list(mapa_anim.keys()), index=None, placeholder="Escribe para buscar...", key="sel_historial")
        
        if seleccion:
            id_anim = mapa_anim[seleccion]
            
            # Llamamos al  endpoint del backend, que devuelve el historial médico completo
            ficha = obtener_historial_animal(id_anim)
            
            if ficha:
                st.markdown("---")
                # Cabecera con datos fijos del paciente
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Paciente", ficha['nombre'])
                c2.metric("Especie", ficha['especie'])
                c3.metric("Raza", ficha['raza'])
                c4.metric("Dueño", ficha['propietario_nombre'])
                
                st.subheader("📅 Historial de Visitas")
                
                if not ficha['citas']:
                    st.info("Este paciente no ha venido a la clínica todavía.")
                else:
                    # Iteramos sobre las citas (que ya vienen ordenadas por fecha desde el backend)
                    for cita in ficha['citas']:
                        # Icono visual según estado
                        icono = "✅" if cita['estado'] == "Realizada" else "⏳" if cita['estado'] == "Pendiente" else "❌"
                        fecha_str = cita['fecha_hora'][:10] # Cortamos la fecha YYYY-MM-DD
                        
                        # Usamos un expander para cada cita, mostrando detalles e informe veterinario si existe
                        with st.expander(f"{icono} {fecha_str} - {cita['motivo']}", expanded=False):
                            col_a, col_b = st.columns([1, 2])
                            
                            with col_a:
                                st.caption("Detalles de la Cita")
                                st.write(f"**Hora:** {cita['fecha_hora'][11:16]}")
                                st.write(f"**Estado:** {cita['estado']}")
                                st.write(f"**Veterinario ID:** {cita['veterinario_id']}")
                            
                            with col_b:
                                st.caption("Informe Veterinario")
                                # Verificamos si hay tratamiento dentro de la cita
                                if cita['tratamiento']:
                                    st.markdown(f"**Diagnóstico:**")
                                    st.success(f"{cita['tratamiento']['diagnostico']}")
                                    st.markdown(f"**Tratamiento / Pauta:**")
                                    st.info(f"{cita['tratamiento']['descripcion']}")
                                else:
                                    st.warning("⚠️ Sin diagnóstico registrado para esta visita.")
            else:
                st.error("Error al cargar el historial médico.")

# Tab 3: NUEVO PACIENTE --> Formulario para ingresar un nuevo paciente
with tab_nuevo:
    st.header("Ingreso de Paciente")
    props = obtener_todos_propietarios()
    
    if not props: # Si no hay propietarios, no podemos crear animales
        st.warning("Primero registra propietarios.")
    else:# Si hay propietarios, mostramos el formulario para crear animales
        mapa_props = {f"{p['nombre']} (ID: {p['id']})": p['id'] for p in props} # Mapa para seleccionar dueño. p es el objeto propietario en la lista
        
        with st.form("form_animal_nuevo"): # Formulario para nuevo animal
            col1, col2 = st.columns(2)
            nom = col1.text_input("Nombre") 
            esp = col2.selectbox("Especie", ["Perro", "Gato", "Ave", "Reptil", "Otro"])
            raz = col1.text_input("Raza")
            ed = col2.number_input("Edad", min_value=0) # solo edades positivas
            dueno = st.selectbox("Dueño", list(mapa_props.keys())) # Selector de dueño, listas de llaves del mapa (nombres)
            
            if st.form_submit_button("Guardar Paciente"): # Botón para enviar el formulario
                datos_nuevos = {
                    "nombre": nom, "especie": esp, "raza": raz, "edad": ed, 
                    "propietario_id": mapa_props[dueno]
                }
                if crear_animal(datos_nuevos): # Llamada a la función de crear animal
                    st.success("Paciente registrado."); st.rerun()

# Tab 4: GESTION --> Editar o borrar animales existentes
with tab_gestion:
    st.header("Modificar Ficha")
    if datos:
        mapa_anim = {f"{a['nombre']} ({a['especie']})": a for a in datos} # Mapa para seleccionar animal, a es el objeto animal en la lista
        sel_anim = st.selectbox("Selecciona Paciente:", list(mapa_anim.keys())) # Selector de animales
        
        if sel_anim: # Si se ha seleccionado un animal, mostramos su información y opciones de edición/borrado
            a_actual = mapa_anim[sel_anim] # Objeto del animal seleccionado
            with st.form("form_editar_animal"): # Formulario para editar animal
                cn1, cn2 = st.columns(2) # Columnas para organizar campos
                n = cn1.text_input("Nombre", value=a_actual['nombre']) # n es el nombre nuevo
                e = cn2.text_input("Especie", value=a_actual['especie']) # e es la especie nueva
                r = cn1.text_input("Raza", value=a_actual['raza']) # r es la raza nueva
                ed = cn2.number_input("Edad", value=a_actual['edad']) # ed es la edad nueva
                # No dejamos cambiar dueño aquí
                
                if st.form_submit_button("💾 Actualizar"): # Botón para enviar formulario de actualización
                    cambios = {"nombre": n, "especie": e, "raza": r, "edad": ed, "propietario_id": a_actual['propietario_id']}
                    if actualizar_animal(a_actual['id'], cambios): # Llamada a la función de actualizar animal
                        st.success("Actualizado"); st.rerun() # Recargamos la página para ver cambios
            
            st.divider() # Línea divisoria para separar secciones
            # Zona de peligro: eliminar animal. Ponemos estas alertas y confirmaciones para evitar borrados accidentales
            with st.expander("🚨 Eliminar Ficha del Paciente"):
                st.write(f"Vas a eliminar a **{a_actual['nombre']}**.")
                
                confirmado_anim = st.checkbox("Entiendo que esta acción es irreversible", key="check_del_anim") # Checkbox de confirmación
                
                # Botón de eliminar, solo activo si se ha confirmado (disabled=not confirmado_anim)
                if st.button("🗑️ Eliminar Paciente", type="primary", disabled=not confirmado_anim, key="btn_del_anim"):
                    if eliminar_animal(a_actual['id']):
                        st.success("Ficha eliminada.")
                        st.rerun() # Recargamos la página para ver cambios