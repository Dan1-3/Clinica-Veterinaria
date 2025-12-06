# Aquí se crearán los esquemas de validación de datos con Pydantic.
# Servirán para definir la estructura de los datos que entran y salen de la API.
from pydantic import BaseModel, ConfigDict

# Esquema base para un animal, despues se usarán para crear y leer animales
class AnimalBase(BaseModel):
    nombre: str
    especie: str
    raza: str
    edad: int
    propietario_id: int  # ID del dueño, clave foránea

class AnimalCreate(AnimalBase): 
# Esta es una clase base para crear un animal, que hereda de AnimalBase y sirve para validación de datos al crear
    pass

class AnimalResponse(AnimalBase): # Esquema para leer un animal, incluye el ID
    id: int
    
    model_config = ConfigDict(from_attributes=True) # Configuración para que se pueda trabajar con SQLAlchemy ORM
      