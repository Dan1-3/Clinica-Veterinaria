# Aquí se programarán las funciones que gestionan la lógica de negocio de los animales.
# Por ejemplo: crear, consultar, listar, actualizar y eliminar animales.

from sqlalchemy.orm import Session
from src.db.models import Animal
from src.schemas.animal_schema import AnimalCreate

class AnimalesService:

    @staticmethod
    def crear_animal(db: Session, animal_data: AnimalCreate):
        nuevo_animal = Animal(**animal_data.model_dump())
        db.add(nuevo_animal)
        db.commit()
        db.refresh(nuevo_animal)
        return nuevo_animal

    @staticmethod
    def listar_animales(db: Session):
        return db.query(Animal).all()

    @staticmethod
    def obtener_animal(db: Session, animal_id: int):
        return db.query(Animal).filter(Animal.id == animal_id).first()
    
    # (PENDIENTE: Agregar lógica de Actualizar y Eliminar en pasos posteriores para mantenerlo simple)