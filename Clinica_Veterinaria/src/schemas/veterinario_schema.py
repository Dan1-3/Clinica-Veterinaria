from pydantic import BaseModel

class VeterinarioBase(BaseModel):
    nombre: str
    apellidos: str
    correo: str
    telefono: str
    horario: str
    cargo: str

class VeterinarioCreate(VeterinarioBase):
    pass

class VeterinarioRead(VeterinarioBase):
    id: int

    class Config:
        from_attributes = True 