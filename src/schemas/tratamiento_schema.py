from pydantic import BaseModel

class TratamientoBase(BaseModel):
    diagnostico: str
    descripcion: str  # Medicamentos, dosis, duración
    cita_id: int      # ID de la cita a la que pertenece este tratamiento

class TratamientoCreate(TratamientoBase):
    pass

class TratamientoRead(TratamientoBase):
    id: int
    class Config:
        from_attributes = True