# Aquí se definen las pruebas unitarias para las funciones de citas.
# Servirán para comprobar que las operaciones CRUD funcionan correctamente.
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import Base

# Importamos TODOS los servicios necesarios para crear una cita completa
from src.services.propietarios_service import PropietariosService
from src.services.animales_service import AnimalesService
from src.services.veterinarios_service import VeterinariosService
from src.services.citas_service import CitasService

# Importamos los esquema de cada entidad para crear los datos necesarios
from src.schemas.propietario_schema import PropietarioCreate
from src.schemas.animal_schema import AnimalCreate
from src.schemas.veterinario_schema import VeterinarioCreate
from src.schemas.cita_schema import CitaCreate

# Misma función para obtener una BD limpia en cada test
def obtener_db_vacia():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

# TEST 1: Crear una cita completa con todas las relaciones
def test_crear_cita_completa():
    db = obtener_db_vacia()
    
    # 1. Crear Dueño
    dueno = PropietariosService.crear_propietario(db, PropietarioCreate(
        nombre="Dueño Cita", email="d@d.com", telefono="600111222", direccion="C"
    ))
    # 2. Crear Animal (del dueño anterior)
    animal = AnimalesService.crear_animal(db, AnimalCreate(
        nombre="Gato", especie="Felino", raza="X", edad=2, propietario_id=dueno.id
    ))
    # 3. Crear Veterinario
    vet = VeterinariosService.crear_veterinario(db, VeterinarioCreate(
        nombre="Dr. House", apellidos="G.", correo="h@v.com", telefono="600333444", horario="M", cargo="Jefe"
    ))
    # 4. Crear Cita relacionando todo lo anterior
    datos_cita = CitaCreate(
        fecha_hora=datetime.now(),
        motivo="Vacuna Anual",
        estado="Pendiente",
        animal_id=animal.id,        # Relación con Animal
        propietario_id=dueno.id,    # Relación con Dueño
        veterinario_id=vet.id       # Relación con Veterinario
    )
    # Crear la cita usando el servicio
    cita = CitasService.crear_cita(db, datos_cita)
    
    # Validaciones de que la cita se creó correctamente y está bien relacionada con todo
    assert cita.id is not None
    assert cita.motivo == "Vacuna Anual"
    assert cita.animal_id == animal.id
    assert cita.veterinario_id == vet.id
    assert cita.estado == "Pendiente"
    assert cita.propietario_id == dueno.id