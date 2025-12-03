# Aquí se crearán los esquemas de validación de datos con Pydantic.
# Servirán para definir la estructura de los datos que entran y salen de la API.
from pydantic import BaseModel

class AnimalBase(BaseModel):
    nombre: str
    especie: str
    raza: str
    edad: int
    propietario_id: int  # IMPRESCINDIBLE: ID del dueño

class AnimalCreate(AnimalBase):
    pass

class AnimalResponse(AnimalBase):
    id: int
    
    class Config:
        from_attributes = True
