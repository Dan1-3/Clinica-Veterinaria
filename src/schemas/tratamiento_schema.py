from pydantic import BaseModel, ConfigDict

class TratamientoBase(BaseModel):
    diagnostico: str # Diagnóstico asociado al tratamiento, descripción breve
    descripcion: str  # Medicamentos, dosis, duración...
    cita_id: int      # ID de la cita a la que pertenece este tratamiento

class TratamientoCreate(TratamientoBase):
    pass

class TratamientoRead(TratamientoBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True) # Configuración para que se pueda trabajar con SQLAlchemy ORM
