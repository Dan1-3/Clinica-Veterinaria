import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import Base
from src.services.veterinarios_service import VeterinariosService
from src.schemas.veterinario_schema import VeterinarioCreate

# Función para tener BD limpia (misma que en tests/test_propietarios.py para mantener aislamiento en cada archivo)
def obtener_db_vacia():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

# TEST 1: Crear un veterinario con todos los datos correctos
def test_registrar_veterinario_correcto():
    db = obtener_db_vacia()
    
    # Preparamos los datos del veterinario, sin errores
    datos = VeterinarioCreate(
        nombre="Laura",
        apellidos="Gomez",
        correo="laura@vet.com",
        telefono="600999888",
        horario="Mañana",
        cargo="Cirujana"
    )
    
    # Creamos el veterinario usando el servicio
    nuevo_vet = VeterinariosService.crear_veterinario(db, datos)
    
    # Verificamos que se guardó la información correctamente
    assert nuevo_vet.id is not None
    assert nuevo_vet.cargo == "Cirujana"
    assert nuevo_vet.horario == "Mañana"
    assert nuevo_vet.apellidos == "Gomez"

# TEST 2: Listar veterinarios, debe devolver lista con al menos uno
def test_listar_veterinarios():
    db = obtener_db_vacia()
    
    # Creamos uno para asegurarnos de que la lista no esté vacía
    datos = VeterinarioCreate(
        nombre="Alex", apellidos="B", correo="c@c.com", 
        telefono="600000000", horario="Tarde", cargo="Auxiliar"
    )
    VeterinariosService.crear_veterinario(db, datos)
    
    # Pedimos la lista al servicio
    lista = VeterinariosService.listar_veterinarios(db)
    
    # Verificamos que la lista tiene al menos un veterinario y es correcto
    assert len(lista) == 1
    assert lista[0].nombre == "Alex"