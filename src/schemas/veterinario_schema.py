from pydantic import BaseModel, ConfigDict

class VeterinarioBase(BaseModel):
    nombre: str
    apellidos: str
    correo: str
    telefono: str
    horario: str
    cargo: str # Rol o cargo del veterinario en la clínica (eg. General, Cirujano...)

class VeterinarioCreate(VeterinarioBase):
    pass

class VeterinarioRead(VeterinarioBase):
    id: int

    model_config = ConfigDict(from_attributes=True) # Configuración para que se pueda trabajar con SQLAlchemy ORM
