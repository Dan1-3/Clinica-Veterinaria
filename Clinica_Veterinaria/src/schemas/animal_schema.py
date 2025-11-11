# Aquí se crearán los esquemas de validación de datos con Pydantic.
# Servirán para definir la estructura de los datos que entran y salen de la API.

from pydantic import BaseModel
from typing import Optional

class AnimalBase(BaseModel):
    nombre: str
    especie: str
    raza: str
    edad: int
    sexo: str

class AnimalCreate(AnimalBase):
    propietario_id: int

class AnimalRead(AnimalBase):
    id: int
    propietario_id: int

    class Config:
        orm_mode = True
