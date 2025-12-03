# Aquí se definirán los endpoints (rutas) de la API relacionados con animales.
# Cada ruta conectará con las funciones del servicio para manejar las peticiones.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.db.database import get_db
from src.schemas.animal_schema import AnimalCreate, AnimalResponse
from src.services.animales_service import AnimalesService

# Definimos el router
router = APIRouter(prefix="/animales", tags=["Animales"])

@router.post("/", response_model=AnimalResponse)
def crear_animal(animal: AnimalCreate, db: Session = Depends(get_db)):
    return AnimalesService.crear_animal(db, animal)

@router.get("/", response_model=List[AnimalResponse])
def listar_animales(db: Session = Depends(get_db)):
    return AnimalesService.listar_animales(db)

@router.get("/{animal_id}", response_model=AnimalResponse)
def obtener_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = AnimalesService.obtener_animal(db, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return animal

@router.delete("/{animal_id}")
def eliminar_animal(animal_id: int, db: Session = Depends(get_db)):
    resultado = AnimalesService.eliminar_animal(db, animal_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return {"message": "Animal eliminado correctamente"}