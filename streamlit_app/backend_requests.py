# Este archivo se encarga del backend de las solicitudes relacionadas con veterinarios.
import requests
import streamlit as st
FASTAPI_URL = "http://127.0.0.1:8000"


# --- PROPIETARIOS  ---
def get_all_propietarios():
    try:
        response = requests.get(f"{FASTAPI_URL}/propietarios/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        st.error("Error al conectar con la API de Propietarios.")
        return []

def create_propietario(data):
    try:
        response = requests.post(f"{FASTAPI_URL}/propietarios/", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        st.error("Error al crear propietario.")
        return None
    
# --- ANIMALES ---

def get_all_animales():
    try:
        response = requests.get(f"{FASTAPI_URL}/animales/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        st.error("Error al conectar con la API de Animales.")
        return []

def create_animal(data):
    try:
        response = requests.post(f"{FASTAPI_URL}/animales/", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        st.error("Error al crear animal.")
        return None
    
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


# --- CITAS ---
def get_all_citas():
    try:
        response = requests.get(f"{FASTAPI_URL}/citas/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        st.error("Error al obtener las citas.")
        return []

# --- TRATAMIENTOS ---
def get_tratamiento_por_cita(cita_id):
    """Busca si existe un tratamiento para una cita concreta"""
    try:
        response = requests.get(f"{FASTAPI_URL}/tratamientos/cita/{cita_id}")
        if response.status_code == 200:
            return response.json()
        return None # Si devuelve 404, es que no hay tratamiento aún
    except requests.exceptions.RequestException:
        return None

def create_tratamiento(data):
    try:
        response = requests.post(f"{FASTAPI_URL}/tratamientos/", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"Error al guardar tratamiento: {response.text}")
        return None