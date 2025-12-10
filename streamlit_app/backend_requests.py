# Este archivo se encarga del backend de las solicitudes relacionadas con veterinarios.
# Se encargan de hacer las peticiones HTTP al servidor FastAPI desde la app Streamlit.
# Cada función corresponde a una operación CRUD (Crear, Leer, Actualizar, Eliminar).

import requests
import streamlit as st

# Dirección de tu servidor (Backend)
URL_API = "http://127.0.0.1:8000"

# ==========================================
# FUNCIONES AUXILIARES: Manejo de errores y respuestas
# ==========================================

def manejar_error_conexion(error): # Maneja errores de conexión al servidor
    st.error(f"⚠️ Error de conexión: No se puede conectar con el servidor.({error})")
    return None

# Procesa la respuesta del servidor y maneja errores comunes: 
    #Analiza lo que responde el servidor.
    #- respuesta: El objeto que devuelve requests.
    #- accion: 'crear', 'actualizar' o 'eliminar'.
    #- tipo_dato: 'Propietario', 'Animal'...

def procesar_respuesta(respuesta, accion, tipo_dato):
    if respuesta.status_code in [200, 201]: # Si todo ha ido bien (Códigos 200 OK o 201 Creado)
        if accion == "eliminar":
            return True # Eliminar no devuelve datos, solo confirmación
        return respuesta.json() # Devolvemos los datos en formato diccionario, para que Streamlit los use
    
    # Si algo ha fallado, intentamos leer el mensaje de detalle del servidor
    try:
        # El backend manda {"detail": "Mensaje de error"}
        detalle_error = respuesta.json().get('detail', respuesta.text)
    except:
        # Si no es JSON, usamos el texto plano. No es json cuando hay errores HTTP genéricos (404, 500...)
        detalle_error = respuesta.text
    
    st.error(f"❌ Error al {accion} {tipo_dato}: {detalle_error}") # Mostramos el error en Streamlit con el detalle
    return None

# ==========================================
# FUNCIONES GENÉRICAS: Principio solid Dependencia Inversa: Funciones reutilizables para CRUD
# ==========================================

# Envía una petición PUT para actualizar un registro.
def enviar_actualizacion(ruta, id_registro, datos_nuevos, nombre_tipo):
    try:
        url_completa = f"{URL_API}/{ruta}/{id_registro}" # URL completa con ID
        respuesta = requests.put(url_completa, json=datos_nuevos) # Petición PUT con los nuevos datos en formato JSON
        return procesar_respuesta(respuesta, "actualizar", nombre_tipo) # Devolvemos el resultado procesado, con el manejo de errores
    except requests.exceptions.RequestException as e:
        return manejar_error_conexion(e)

# Envía una petición DELETE para eliminar un registro.
def enviar_eliminacion(ruta, id_registro, nombre_tipo):
    try:
        url_completa = f"{URL_API}/{ruta}/{id_registro}" # URL completa con ID
        respuesta = requests.delete(url_completa) # Petición DELETE para eliminar el registro
        return procesar_respuesta(respuesta, "eliminar", nombre_tipo) # Devolvemos el resultado procesado, con el manejo de errores
    except requests.exceptions.RequestException as e:
        return manejar_error_conexion(e)

# ==========================================
#  1. GESTIÓN DE PROPIETARIOS
# ==========================================

# Obtener todos los propietarios (GET)
def obtener_todos_propietarios():
    try:
        respuesta = requests.get(f"{URL_API}/propietarios/") # Petición GET para obtener todos los propietarios
        if respuesta.status_code == 200: # Si todo ha ido bien (200 OK) devolvemos los datos
            return respuesta.json()
        return []
    except requests.exceptions.RequestException: # Si hay error de conexión, mostramos mensaje y devolvemos lista vacía
        st.error("No se pudieron cargar los propietarios.")
        return []
    
# Obtener ficha completa de un propietario (GET)
def obtener_ficha_propietario(id_propietario):
    try:
        # Petición al nuevo endpoint que agrupa todos los datos
        respuesta = requests.get(f"{URL_API}/propietarios/{id_propietario}/ficha")
        if respuesta.status_code == 200:
            return respuesta.json()
        return None
    except requests.exceptions.RequestException as e:
        return manejar_error_conexion(e)

# Crear un nuevo propietario (POST)
def crear_propietario(datos):
    try:
        respuesta = requests.post(f"{URL_API}/propietarios/", json=datos)
        return procesar_respuesta(respuesta, "crear", "Propietario")
    except requests.exceptions.RequestException as e:
        return manejar_error_conexion(e)

# Actualizar un propietario (PUT)
def actualizar_propietario(id_propietario, datos_nuevos):
    return enviar_actualizacion("propietarios", id_propietario, datos_nuevos, "Propietario")

# Eliminar un propietario (DELETE)
def eliminar_propietario(id_propietario):
    return enviar_eliminacion("propietarios", id_propietario, "Propietario")

# ==========================================
# 2. GESTIÓN DE ANIMALES
# ==========================================

# Obtener todos los animales (GET)
def obtener_todos_animales():
    try:
        respuesta = requests.get(f"{URL_API}/animales/")
        if respuesta.status_code == 200:
            return respuesta.json()
        return []
    except requests.exceptions.RequestException:
        st.error("No se pudieron cargar los animales.")
        return []
    
# Obtener historial médico de un animal (GET)
def obtener_historial_animal(id_animal):
    try:
        r = requests.get(f"{URL_API}/animales/{id_animal}/historial")
        return r.json() if r.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        return manejar_error_conexion(e)

# Crear un nuevo animal (POST)
def crear_animal(datos):
    try:
        respuesta = requests.post(f"{URL_API}/animales/", json=datos)
        return procesar_respuesta(respuesta, "crear", "Animal")
    except requests.exceptions.RequestException as e:
        return manejar_error_conexion(e)

# Actualizar un animal (PUT)
def actualizar_animal(id_animal, datos_nuevos):
    return enviar_actualizacion("animales", id_animal, datos_nuevos, "Animal")

# Eliminar un animal (DELETE)
def eliminar_animal(id_animal):
    return enviar_eliminacion("animales", id_animal, "Animal")

# ==========================================
# 3. GESTIÓN DE VETERINARIOS
# ==========================================

# Obtener todos los veterinarios (GET)
def obtener_todos_veterinarios():
    try:
        respuesta = requests.get(f"{URL_API}/veterinarios/")
        if respuesta.status_code == 200:
            return respuesta.json()
        return []
    except requests.exceptions.RequestException:
        st.error("No se pudieron cargar los veterinarios.")
        return []

# Crear un nuevo veterinario (POST)
def crear_veterinario(datos):
    try:
        respuesta = requests.post(f"{URL_API}/veterinarios/", json=datos)
        return procesar_respuesta(respuesta, "crear", "Veterinario")
    except requests.exceptions.RequestException as e:
        return manejar_error_conexion(e)

# ==========================================
# 4. GESTIÓN DE CITAS
# ==========================================

# Obtener todas las citas (GET)
def obtener_todas_citas():
    try:
        respuesta = requests.get(f"{URL_API}/citas/")
        if respuesta.status_code == 200:
            return respuesta.json()
        return []
    except requests.exceptions.RequestException:
        st.error("No se pudieron cargar las citas.")
        return []

# ==========================================
# 5. GESTIÓN DE TRATAMIENTOS
# ==========================================

# Obtener tratamiento por ID de cita (GET)
def obtener_tratamiento_por_cita(id_cita):
    try:
        # Petición GET a /tratamientos/cita/{id}
        respuesta = requests.get(f"{URL_API}/tratamientos/cita/{id_cita}")
        if respuesta.status_code == 200:
            return respuesta.json()
        return None # Si da 404 es que no existe
    except requests.exceptions.RequestException:
        return None

# Crear un nuevo tratamiento (POST)
def crear_tratamiento(datos):
    try:
        respuesta = requests.post(f"{URL_API}/tratamientos/", json=datos)
        return procesar_respuesta(respuesta, "crear", "Tratamiento")
    except requests.exceptions.RequestException as e:
        return manejar_error_conexion(e)

# Actualizar un tratamiento (PUT)
def actualizar_tratamiento(id_tratamiento, datos_nuevos):
    return enviar_actualizacion("tratamientos", id_tratamiento, datos_nuevos, "Tratamiento")

# Eliminar un tratamiento (DELETE)
def eliminar_tratamiento(id_tratamiento):
    return enviar_eliminacion("tratamientos", id_tratamiento, "Tratamiento")