import streamlit as st
from streamlit_app.backend_requests import obtener_todas_citas, obtener_tratamiento_por_cita, crear_tratamiento, actualizar_tratamiento, eliminar_tratamiento

# Configuración de la página
st.set_page_config(page_title="Tratamientos", page_icon="💊")
st.title("💊 Diagnóstico y Tratamientos")

# 1. CARGAR DATOS --> Obtener todas las citas
citas = obtener_todas_citas()

# 2. SELECCIÓN DE CITA Y GESTIÓN DE TRATAMIENTO
if not citas:
    st.info("ℹ️ No hay citas registradas. Ve a la sección de 'Citas' para crear una.")
else:
    st.info("Selecciona una cita para ver, crear o editar su informe clínico.")
    
    # Selector de citas: diccionario de opciones "Cita #ID - Motivo (Estado)" -> ID
    opciones = {f"Cita #{c['id']} - {c['motivo']} (Estado: {c['estado']})": c['id'] for c in citas}
    seleccion = st.selectbox("Pacientes en espera / atendidos:", list(opciones.keys())) # Selector desplegable de citas con las opciones anteriores
    
    if seleccion: 
        cita_id = opciones[seleccion] # ID de la cita seleccionada
        
        # Buscamos si ya tiene tratamiento
        tratamiento = obtener_tratamiento_por_cita(cita_id)
        st.markdown("---") # Separador visual

        # CASO A: YA TIENE TRATAMIENTO (VER / EDITAR / BORRAR) 
        if tratamiento:
            st.success("✅ Esta cita ya tiene un informe cerrado.")
            
            # Editar tratamiento existente
            with st.expander("📝 Ver / Editar Informe", expanded=True):
                with st.form("form_editar_tratamiento"):
                    diag = st.text_area("Diagnóstico", value=tratamiento['diagnostico']) # Campo de texto para diagnóstico nuevo
                    desc = st.text_area("Tratamiento", value=tratamiento['descripcion']) # Campo de texto para tratamiento nuevo
                    
                    col1, col2 = st.columns([1, 1])
                    update_btn = col1.form_submit_button("💾 Actualizar Informe")
                    
                    if update_btn:
                        datos_nuevos = {
                            "diagnostico": diag, 
                            "descripcion": desc, 
                            "cita_id": cita_id
                        }
                        if actualizar_tratamiento(tratamiento['id'], datos_nuevos):
                            st.toast("Informe actualizado correctamente") # Notificación pequeña. toast es un mensaje emergente que desaparece solo
                            st.rerun()

            st.divider()

            # Zona de peligro (borrado seguro) --> Eliminar tratamiento existente pero con confirmación, para evitar borrados accidentales
            with st.expander("🚨 Zona de Peligro - Eliminar Informe"):
                st.warning("Si borras este informe, la cita volverá a estar 'sin diagnóstico'.")
                
                # Checkbox de seguridad
                confirmado = st.checkbox("Entiendo que esta acción es irreversible", key="check_del_trat")
                
                # El botón solo funciona si el checkbox está marcado
                if st.button("🗑️ Eliminar Informe Definitivamente", type="primary", disabled=not confirmado):
                    if eliminar_tratamiento(tratamiento['id']):
                        st.success("Informe eliminado correctamente.")
                        st.rerun()

        # CASO B: NO TIENE TRATAMIENTO (CREAR) 
        else:
            st.warning("⚠️ Esta cita está pendiente de diagnóstico.")
            
            with st.form("form_nuevo_tratamiento"):
                st.subheader("Redactar Nuevo Informe")
                diag = st.text_area("Diagnóstico Veterinario", placeholder="Ej: Gastroenteritis leve...") # Campo de texto para diagnóstico nuevo, ponemos en placeholder un ejemplo para guiar al usuario. 
                # placeholder es un texto que aparece en el campo cuando está vacío
                desc = st.text_area("Pauta / Medicación", placeholder="Ej: Dieta blanda 3 días...") # Campo de texto para tratamiento nuevo, ponemos en placeholder un ejemplo para guiar al usuario. placeholder es un texto que aparece en el campo cuando está vacío
                if st.form_submit_button("Guardar Informe"):
                    datos = {
                        "diagnostico": diag, 
                        "descripcion": desc, 
                        "cita_id": cita_id
                    }
                    if crear_tratamiento(datos):
                        st.balloons() # Efecto visual de globos al crear el tratamiento, no interfiere con la lógica del programa
                        st.success("Tratamiento registrado con éxito.")
                        st.rerun()