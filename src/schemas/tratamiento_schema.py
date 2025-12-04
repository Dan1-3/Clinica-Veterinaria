from pydantic import BaseModel

class TratamientoBase(BaseModel):
    diagnostico: str # Diagnóstico asociado al tratamiento, descripción breve
    descripcion: str  # Medicamentos, dosis, duración...
    cita_id: int      # ID de la cita a la que pertenece este tratamiento

class TratamientoCreate(TratamientoBase):
    pass

class TratamientoRead(TratamientoBase):
    id: int
    class Config: # Configuración para que pydantic pueda trabajar con ORM (SQLAlchemy)
        orm_mode = True