from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.db.database import get_db
from src.schemas.propietario_schema import PropietarioCreate, PropietarioResponse
from src.services.propietarios_service import PropietariosService

# Definimos el router
router = APIRouter(prefix="/propietarios", tags=["Propietarios"])

# 1. CREAR
@router.post("/", response_model=PropietarioResponse)
def crear_propietario(propietario: PropietarioCreate, db: Session = Depends(get_db)):
    return PropietariosService.crear_propietario(db, propietario)

# 2. LISTAR TODOS
@router.get("/", response_model=List[PropietarioResponse])
def listar_propietarios(db: Session = Depends(get_db)):
    return PropietariosService.listar_propietarios(db)

# 3. OBTENER UNO
@router.get("/{propietario_id}", response_model=PropietarioResponse)
def obtener_propietario(propietario_id: int, db: Session = Depends(get_db)):
    db_propietario = PropietariosService.obtener_propietario(db, propietario_id)
    if db_propietario is None:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return db_propietario

# 4. ACTUALIZAR
@router.put("/{propietario_id}", response_model=PropietarioResponse)
def actualizar_propietario(propietario_id: int, nuevos_datos: PropietarioCreate, db: Session = Depends(get_db)):
    propietario = PropietariosService.actualizar_propietario(db, propietario_id, nuevos_datos)
    if propietario is None:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return propietario

# 5 ELIMINAR
@router.delete("/{propietario_id}")
def eliminar_propietario(propietario_id: int, db: Session = Depends(get_db)):
    resultado = PropietariosService.eliminar_propietario(db, propietario_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return {"message": "Propietario eliminado correctamente"}