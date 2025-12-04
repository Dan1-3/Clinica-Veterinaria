# Este archivo se encarga del backend de las solicitudes relacionadas con veterinarios.
# Se encargan de hacer las peticiones HTTP al servidor FastAPI desde la app Streamlit.
# Cada función corresponde a una operación CRUD (Crear, Leer, Actualizar, Eliminar).

import requests
import streamlit as st

# URL del Backend (FastAPI), para hacer las peticiones
FASTAPI_URL = "http://127.0.0.1:8000"

# ==========================================
# FUNCIONES GENERALES DE MANEJO DE RESPUESTAS
# Funciones para manejar respuestas y errores de las solicitudes HTTP, que después se usan en las funciones CRUD
# ==========================================

# Procesa la respuesta del servidor para creaciones (POST) y devuelve el JSON si todo va bien, o None si hay error.
def manejar_respuesta_post(response, entidad_nombre):
    # 1. Si es éxito (200 OK o 201 Created)
    if response.status_code in [200, 201]:
        return response.json()
    
    # 2. Si hay error, intentamos leer el detalle para mostrarlo
    try:
        error_detail = response.json().get('detail', response.text)
    except:
        error_detail = response.text # Si no es JSON, texto crudo
    
    # Mostramos el error explicativo en pantalla roja
    st.error(f"❌ Error al guardar {entidad_nombre}: {error_detail}")
    return None

def manejar_error_conexion(e):
    st.error(f"⚠️ Error de conexión: No se puede contactar con el servidor. ¿Está encendido el Backend? ({e})")
    return None

# ==========================================
# PROPIETARIOS
# ==========================================

# Obtener todos los propietarios (GET): devuelve lista de propietarios o vacía si hay error
def get_all_propietarios():
    try:
        response = requests.get(f"{FASTAPI_URL}/propietarios/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener propietarios ({response.status_code})")
            return []
    except requests.exceptions.RequestException as e:
        manejar_error_conexion(e)
        return []

# Crear un nuevo propietario (POST): devuelve el propietario creado o None si hay error
def create_propietario(data):
    try:
        response = requests.post(f"{FASTAPI_URL}/propietarios/", json=data)
        return manejar_respuesta_post(response, "Propietario")
    except requests.exceptions.RequestException as e:
        return manejar_error_conexion(e)

# ==========================================
# ANIMALES
# ==========================================
# Obtener todos los animales (GET): devuelve lista de animales o vacía si hay error
def get_all_animales():
    try:
        response = requests.get(f"{FASTAPI_URL}/animales/")
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException as e:
        manejar_error_conexion(e)
        return []

# Crear un nuevo animal (POST): devuelve el animal creado o None si hay error
def create_animal(data):
    try:
        response = requests.post(f"{FASTAPI_URL}/animales/", json=data)
        return manejar_respuesta_post(response, "Animal")
    except requests.exceptions.RequestException as e:
        return manejar_error_conexion(e)

# ==========================================
# VETERINARIOS
# ==========================================

# Obtener todos los veterinarios (GET): devuelve lista de veterinarios o vacía si hay error
def get_all_veterinarios():
    try:
        response = requests.get(f"{FASTAPI_URL}/veterinarios/")
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException as e:
        manejar_error_conexion(e)
        return []

# Crear un nuevo veterinario (POST): devuelve el veterinario creado o None si hay error
def create_veterinario(data):
    try:
        response = requests.post(f"{FASTAPI_URL}/veterinarios/", json=data)
        return manejar_respuesta_post(response, "Veterinario")
    except requests.exceptions.RequestException as e:
        return manejar_error_conexion(e)

# ==========================================
# CITAS
# ==========================================

# Obtener todas las citas (GET): devuelve lista de citas o vacía si hay error
def get_all_citas():
    try:
        response = requests.get(f"{FASTAPI_URL}/citas/")
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException as e:
        manejar_error_conexion(e)
        return []

# Añadimos create_cita para que sea consistente, devuelve la cita creada o None si hay error
def create_cita(data):
    try:
        response = requests.post(f"{FASTAPI_URL}/citas/", json=data)
        return manejar_respuesta_post(response, "Cita")
    except requests.exceptions.RequestException as e:
        return manejar_error_conexion(e)

# ==========================================
# TRATAMIENTOS
# ==========================================
# Obtener tratamiento por cita (GET): devuelve el tratamiento o None si no existe o hay error
def get_tratamiento_por_cita(cita_id):
    try:
        response = requests.get(f"{FASTAPI_URL}/tratamientos/cita/{cita_id}")
        if response.status_code == 200:
            return response.json()
        return None # 404 significa que no hay tratamiento, no es un error de conexión
    except requests.exceptions.RequestException:
        return None

# Crear un nuevo tratamiento (POST): devuelve el tratamiento creado o None si hay error
def create_tratamiento(data):
    try:
        response = requests.post(f"{FASTAPI_URL}/tratamientos/", json=data)
        return manejar_respuesta_post(response, "Tratamiento")
    except requests.exceptions.RequestException as e:
        return manejar_error_conexion(e)