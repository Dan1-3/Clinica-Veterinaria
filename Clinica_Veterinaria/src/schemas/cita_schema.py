from pydantic import BaseModel
from datetime import datetime

class CitaBase(BaseModel):
    fecha_hora: datetime
    motivo: str
    estado: str

class CitaCreate(CitaBase):
    animal_id: int
    propietario_id: int
    veterinario_id: int

class CitaRead(CitaBase):
    id: int
    animal_id: int
    propietario_id: int
    veterinario_id: int

    class Config:
        orm_mode = True
