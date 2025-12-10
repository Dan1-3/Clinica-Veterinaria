# Aquí se crearán los esquemas de validación de datos con Pydantic.
# Servirán para definir la estructura de los datos que entran y salen de la API.
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

# Esquema base para un animal, despues se usarán para crear y leer animales
class AnimalBase(BaseModel):
    nombre: str
    especie: str
    raza: str
    edad: int
    propietario_id: int  # ID del dueño, clave foránea

class AnimalCreate(AnimalBase): 
# Esta es una clase base para crear un animal, que hereda de AnimalBase y sirve para validación de datos al crear
    pass

class AnimalResponse(AnimalBase): # Esquema para leer un animal, incluye el ID
    id: int
    
    model_config = ConfigDict(from_attributes=True) # Configuración para que se pueda trabajar con SQLAlchemy ORM


# 1. Tratamiento dentro del historial
class TratamientoHistorial(BaseModel):
    diagnostico: str
    descripcion: str
    model_config = ConfigDict(from_attributes=True)

# 2. Cita dentro del historial del animal
class CitaHistorial(BaseModel):
    id: int
    fecha_hora: datetime
    motivo: str
    estado: str
    veterinario_id: int
    tratamiento: Optional[TratamientoHistorial] = None 
    model_config = ConfigDict(from_attributes=True)

# 3. La Ficha Completa del Animal
class AnimalFichaMedica(AnimalResponse):
    propietario_nombre: Optional[str] = None # Nombre del dueño para mostrarlo fácil
    citas: List[CitaHistorial] = []
    model_config = ConfigDict(from_attributes=True)