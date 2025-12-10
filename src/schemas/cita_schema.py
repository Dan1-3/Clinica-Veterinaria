from pydantic import BaseModel, ConfigDict
from datetime import datetime # Aqui si importamos datetime para las citas, pues necesitamos que tenga fecha y hora

# Clase abstracta base para las citas
class CitaBase(BaseModel):
    fecha_hora: datetime
    motivo: str # Motivo de la cita: Descripción breve
    estado: str # Estado de la cita: Pendiente, Completada, Cancelada

# Clase para crear una cita, hereda de CitaBase
class CitaCreate(CitaBase):
    animal_id: int
    propietario_id: int
    veterinario_id: int

# Clase para leer una cita, incluye el ID y las claves foráneas
class CitaRead(CitaBase):
    id: int
    animal_id: int
    propietario_id: int
    veterinario_id: int

    model_config = ConfigDict(from_attributes=True) # Configuración para que se pueda trabajar con SQLAlchemy ORM 
