from pydantic import BaseModel

class PropietarioBase(BaseModel):
    nombre: str
    email: str
    telefono: str
    direccion: str

class PropietarioCreate(PropietarioBase):
    pass

class PropietarioResponse(PropietarioBase):
    id: int
    
    class Config:
        orm_mode = True