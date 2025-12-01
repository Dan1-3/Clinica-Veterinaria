# Este archivo se encarga del backend de las solicitudes relacionadas con veterinarios.
import requests
import streamlit as st
FASTAPI_URL = "http://127.0.0.1:8000"

# --- VETERINARIOS ---
def get_all_veterinarios():
    try:
        response = requests.get(f"{FASTAPI_URL}/veterinarios/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener veterinarios: {e}")
        return []

def create_veterinario(data):
    try:
        response = requests.post(f"{FASTAPI_URL}/veterinarios/", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"Error al crear veterinario: {response.json().get('detail', 'Error desconocido')}")
        return None