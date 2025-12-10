# Aquí se definirán los endpoints (rutas) de la API relacionados con animales.
# Cada ruta conectará con las funciones del servicio para manejar las peticiones.

from fastapi import APIRouter, Depends, HTTPException # crear rutas y manejar dependencias/excepciones
from sqlalchemy.orm import Session # manejar sesiones de base de datos
from typing import List # definir listas en las respuestas

from src.db.database import get_db # obtener la sesión (conexion) de la base de datos
from src.schemas.animal_schema import AnimalCreate, AnimalResponse,  AnimalFichaMedica # esquemas de validación de datos
from src.services.animales_service import AnimalesService # funciones de negocio para animales

# Definimos el router, que es un conjunto de rutas relacionadas con animales
router = APIRouter(prefix="/animales", tags=["Animales"])

# 1. Endpoint CREAR (POST)
@router.post("/", response_model=AnimalResponse)
def crear_animal(animal: AnimalCreate, db: Session = Depends(get_db)):
    return AnimalesService.crear_animal(db, animal)

# 2. Endpoint LISTAR TODOS (GET)
@router.get("/", response_model=List[AnimalResponse])
def listar_animales(db: Session = Depends(get_db)):
    return AnimalesService.listar_animales(db)

# 3. Endpoint OBTENER UNO (GET)
@router.get("/{animal_id}", response_model=AnimalResponse)
def obtener_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = AnimalesService.obtener_animal(db, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return animal

# 4. Endpoint ELIMINAR (DELETE)
@router.delete("/{animal_id}")
def eliminar_animal(animal_id: int, db: Session = Depends(get_db)):
    resultado = AnimalesService.eliminar_animal(db, animal_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return {"message": "Animal eliminado correctamente"}

# 5. Endpoint FICHA CLINICA COMPLETA DEL ANIMAL (GET)

@router.get("/{animal_id}/historial", response_model=AnimalFichaMedica)
def obtener_historial_medico(animal_id: int, db: Session = Depends(get_db)):
    ficha = AnimalesService.obtener_ficha_clinica(db, animal_id)
    if not ficha:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return ficha

# 6. Endpoint ACTUALIZAR (PUT)

@router.put("/{animal_id}", response_model=AnimalResponse) 
def actualizar_animal(animal_id: int, animal: AnimalCreate, db: Session = Depends(get_db)):
    # Llamamos al servicio (asegúrate de importar HTTPException si da error)
    try:
        return AnimalesService.actualizar_animal(db, animal_id, animal)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No se pudo actualizar: {str(e)}")
