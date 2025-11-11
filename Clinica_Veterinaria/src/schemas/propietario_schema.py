from pydantic import BaseModel
from typing import Optional, List

class PropietarioBase(BaseModel):
    nombre: str
    apellidos: str
    telefono: str
    direccion: str
    correo: str

class PropietarioCreate(PropietarioBase):
    pass

class PropietarioRead(PropietarioBase):
    id: int

    class Config:
        orm_mode = True
