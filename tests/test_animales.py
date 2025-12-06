# Aquí se definen las pruebas unitarias para las funciones de animales.
# Servirán para comprobar que las operaciones CRUD funcionan correctamente.

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import Base

# Importamos servicios de Propietarios y Animales, 
# ya que para crear un animal necesitamos un propietario existente
from src.services.propietarios_service import PropietariosService
from src.services.animales_service import AnimalesService
from src.schemas.propietario_schema import PropietarioCreate
from src.schemas.animal_schema import AnimalCreate

# Misma función para obtener una BD limpia en cada test
def obtener_db_vacia():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

# TEST 1: Crear animal asociado a un dueño existente
def test_crear_animal_con_dueno():
    db = obtener_db_vacia()
    
    # 1. Primero creamos al dueño (Requisito obligatorio para crear el animal)
    datos_dueno = PropietarioCreate(
        nombre="Pedro", 
        email="pedro@email.com", 
        telefono="600111222", 
        direccion="Casa"
    )
    dueno = PropietariosService.crear_propietario(db, datos_dueno)
    
    # 2. Ahora creamos al animal usando el ID del dueño creado
    datos_animal = AnimalCreate(
        nombre="Toby",
        especie="Perro",
        raza="Pastor Aleman",
        edad=5,
        propietario_id=dueno.id # Relacionamos con el dueño creado previamente
    )
    
    animal = AnimalesService.crear_animal(db, datos_animal)
    
    # Validaciones de que el animal se creó correctamente y está asociado al dueño
    assert animal.id is not None
    assert animal.nombre == "Toby"
    assert animal.propietario_id == dueno.id # Confirmamos la relación correcta