import streamlit as st
import pandas as pd
from streamlit_app.backend_requests import get_all_citas, get_tratamiento_por_cita, create_tratamiento

st.title("💊 Gestión de Tratamientos")
st.markdown("---")

# 1. SELECCIONAR CITA
st.subheader("Seleccionar Cita Médica")
lista_citas = get_all_citas()

if not lista_citas:
    st.info("No hay citas registradas para tratar.")
else:
    # Creamos un selector amigable: "ID: 1 - Fecha: ... - Motivo: ..."
    opciones_citas = {f"Cita #{c['id']} | {c['fecha_hora']} | {c['motivo']}": c['id'] for c in lista_citas}
    seleccion = st.selectbox("Elige una cita para diagnosticar:", list(opciones_citas.keys()))
    
    if seleccion:
        cita_id_seleccionada = opciones_citas[seleccion]
        
        # 2. COMPROBAR SI YA TIENE TRATAMIENTO
        tratamiento_existente = get_tratamiento_por_cita(cita_id_seleccionada)
        
        if tratamiento_existente:
            # --- MODO LECTURA (Ya existe) ---
            st.success("✅ Esta cita ya tiene un diagnóstico registrado.")
            st.warning(f"Diagnóstico: {tratamiento_existente['diagnostico']}")
            st.info(f"Tratamiento: {tratamiento_existente['descripcion']}")
            
        else:
            # --- MODO ESCRITURA (Nuevo) ---
            st.header("📝 Registrar Nuevo Diagnóstico")
            with st.form("form_tratamiento"):
                diagnostico = st.text_area("Diagnóstico Veterinario")
                descripcion = st.text_area("Descripción del Tratamiento (Medicamentos, pautas...)")
                
                submitted = st.form_submit_button("Guardar Informe")
                
                if submitted:
                    datos = {
                        "diagnostico": diagnostico,
                        "descripcion": descripcion,
                        "cita_id": cita_id_seleccionada
                    }
                    nuevo = create_tratamiento(datos)
                    if nuevo:
                        st.success("Tratamiento registrado correctamente.")
                        st.rerun()