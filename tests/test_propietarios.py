# Los codigos de pruebas estan soportados e implementados en src/services/propietarios_service.py
# Aquí se escribirán las pruebas unitarias para las funciones de propietarios.
# Servirán para comprobar que las operaciones CRUD funcionan correctamente.

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException

# Importamos los esquemas y servicios de propietarios
from src.db.database import Base
from src.services.propietarios_service import PropietariosService
from src.schemas.propietario_schema import PropietarioCreate

# Función simple para tener una BD limpia en cada test --> sirve para hacer pruebas de manera aislada
def obtener_db_vacia():
    engine = create_engine("sqlite:///:memory:") # Base de datos en memoria para pruebas
    Base.metadata.create_all(engine) # Crear las tablas
    Session = sessionmaker(bind=engine) # Crear la sesión
    return Session() # Devolver la sesión de la base de datos limpia

# TEST 1: Crear propietario correctamente, con datos válidos
def test_crear_propietario_correcto():
    db = obtener_db_vacia()
    
    # Datos correctos
    datos = PropietarioCreate(
        nombre="Juan", 
        email="juan@correo.com", 
        telefono="600123456", 
        direccion="Calle Real 1"
    )
    
    nuevo_propietario = PropietariosService.crear_propietario(db, datos)
    
    # Verificamos que el propietario se creó correctamente, con los datos esperados
    assert nuevo_propietario.id is not None
    assert nuevo_propietario.nombre == "Juan"
    assert nuevo_propietario.email == "juan@correo.com"

# TEST 2: Crear propietario con email incorrecto (sin @)
def test_fallo_email_incorrecto():
    db = obtener_db_vacia()
    
    # Datos con email sin @
    datos_malos = PropietarioCreate(
        nombre="Pepe", 
        email="esto_no_es_un_email", 
        telefono="600123456", 
        direccion="Calle Falsa"
    )
    
    # Verificamos que salta el error HTTPException correctamente
    with pytest.raises(HTTPException) as error:
        PropietariosService.crear_propietario(db, datos_malos)
    
    # Comprobamos que el código de error y el mensaje son los esperados
    assert error.value.status_code == 400
    assert "correo" in error.value.detail

# TEST 3: Crear propietario con teléfono incorrecto (no empieza por 6)
def test_fallo_telefono_incorrecto():
    db = obtener_db_vacia()
    
    # Datos con teléfono que no empieza por 6
    datos_malos = PropietarioCreate(
        nombre="Ana", 
        email="ana@correo.com", 
        telefono="123456789", # Mal, no empieza por 6
        direccion="Calle Falsa"
    )
    
    # Verificamos que salta el error HTTPException correctamente
    with pytest.raises(HTTPException) as error:
        PropietariosService.crear_propietario(db, datos_malos)
   
    # Comprobamos que el código de error es el esperado
    assert error.value.status_code == 400