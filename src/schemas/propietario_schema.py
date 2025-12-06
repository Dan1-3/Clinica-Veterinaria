from pydantic import BaseModel, ConfigDict

class PropietarioBase(BaseModel):
    nombre: str
    email: str
    telefono: str
    direccion: str

class PropietarioCreate(PropietarioBase):
    pass

class PropietarioResponse(PropietarioBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True) # Configuración para que se pueda trabajar con SQLAlchemy ORM
