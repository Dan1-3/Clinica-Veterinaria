from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

# Esquema base para un propietario
class PropietarioBase(BaseModel):
    nombre: str
    email: str
    telefono: str
    direccion: str

class PropietarioCreate(PropietarioBase):
    pass

class PropietarioResponse(PropietarioBase):
    id: int
    model_config = ConfigDict(from_attributes=True) #Configuracion para trabajar con ORM/SQLAlchemy


# 1. Esquema  de Cita para ver dentro de la ficha
class CitaEnFicha(BaseModel):
    id: int
    fecha_hora: datetime
    motivo: str
    estado: str
    model_config = ConfigDict(from_attributes=True)

# 2. Esquema de Animal que incluye sus citas
class AnimalEnFicha(BaseModel):
    id: int
    nombre: str
    especie: str
    raza: str
    edad: int
    # Lista de citas de este animal
    citas: List[CitaEnFicha] = [] 
    model_config = ConfigDict(from_attributes=True)

# 3. Esquema de Propietario que incluye sus animales (y estos sus citas)
class PropietarioFichaCompleta(PropietarioResponse):
    animales: List[AnimalEnFicha] = []
    model_config = ConfigDict(from_attributes=True)