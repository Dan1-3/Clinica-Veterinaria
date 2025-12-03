# Aquí se programarán las funciones que gestionan la lógica de negocio de los animales.
# Por ejemplo: crear, consultar, listar, actualizar y eliminar animales.

from sqlalchemy.orm import Session
from src.db.models import Animal
from src.schemas.animal_schema import AnimalCreate

class AnimalesService:
    
    # 1. CREAR
    @staticmethod
    def crear_animal(db: Session, animal: AnimalCreate):
        nuevo_animal = Animal(
            nombre=animal.nombre,
            especie=animal.especie,
            raza=animal.raza,
            edad=animal.edad,
            propietario_id=animal.propietario_id
        )
        db.add(nuevo_animal)
        db.commit()
        db.refresh(nuevo_animal)
        return nuevo_animal

    # 2. LISTAR TODOS
    @staticmethod
    def listar_animales(db: Session):
        return db.query(Animal).all()

    # 3. OBTENER UNO
    @staticmethod
    def obtener_animal(db: Session, animal_id: int):
        return db.query(Animal).filter(Animal.id == animal_id).first()

    # 4. ELIMINAR
    @staticmethod
    def eliminar_animal(db: Session, animal_id: int):
        animal = db.query(Animal).filter(Animal.id == animal_id).first()
        if animal:
            db.delete(animal)
            db.commit()
            return True
        return False