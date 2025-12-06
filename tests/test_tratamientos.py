# Aquí se definen las pruebas unitarias para las funciones de tratamientos.
# Servirán para comprobar que las operaciones CRUD funcionan correctamente.
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import Base
from src.db.models import Cita, Animal, Propietario, Veterinario # Importamos modelos para crear datos rápido
from src.services.tratamientos_service import TratamientosService
from src.schemas.tratamiento_schema import TratamientoCreate

# Misma función para obtener una BD limpia en cada test
def obtener_db_vacia():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

# TEST 1: Crear un tratamiento asociado a una cita existente
def test_crear_tratamiento_para_cita():
    db = obtener_db_vacia()
    
# Creamos los datos mínimos necesarios para que exista una cita
    db.add(Propietario(id=1, nombre="P", email="p@p.com", telefono="600000000", direccion="D"))
    db.add(Veterinario(id=1, nombre="V", email="v@v.com", telefono="600000000"))
    db.add(Animal(id=1, nombre="A", especie="E", raza="R", edad=1, propietario_id=1))
    db.add(Cita(id=1, animal_id=1, veterinario_id=1, propietario_id=1, motivo="Dolor"))
    db.commit()
    
    # Datos del tratamiento asociado a la cita creada
    datos_tratamiento = TratamientoCreate(
        diagnostico="Gripe canina",
        descripcion="Reposo y mucha agua",
        cita_id=1 # Asociamos a la cita creada arriba
    )
    # Creamos el tratamiento usando el servicio
    tratamiento = TratamientosService.crear_tratamiento(db, datos_tratamiento)
    
    # Validaciones de que el tratamiento se creó correctamente y está asociado a la cita
    assert tratamiento.id is not None
    assert tratamiento.diagnostico == "Gripe canina"
    assert tratamiento.cita_id == 1