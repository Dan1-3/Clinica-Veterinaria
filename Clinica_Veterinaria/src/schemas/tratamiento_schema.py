from pydantic import BaseModel

class TratamientoBase(BaseModel):
    diagnostico: str
    descripcion: str
    medicamentos: str
    duracion: str

class TratamientoCreate(TratamientoBase):
    cita_id: int

class TratamientoRead(TratamientoBase):
    id: int
    cita_id: int

    class Config:
        orm_mode = True
