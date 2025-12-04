from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.schemas.tratamiento_schema import TratamientoCreate, TratamientoRead
from src.services.tratamientos_service import TratamientosService

# Definimos el router
router = APIRouter(prefix="/tratamientos", tags=["Tratamientos"])

# 1. Endpoint CREAR (POST)
@router.post("/", response_model=TratamientoRead)
def crear_tratamiento(tratamiento: TratamientoCreate, db: Session = Depends(get_db)):
    return TratamientosService.crear_tratamiento(db, tratamiento)

# 2. Endpoint OBTENER TRATAMIENTO POR CITA (GET)
@router.get("/cita/{cita_id}", response_model=TratamientoRead)
def obtener_tratamiento_por_cita(cita_id: int, db: Session = Depends(get_db)):
    tratamiento = TratamientosService.obtener_por_cita(db, cita_id)
    if not tratamiento:
        raise HTTPException(status_code=404, detail="No existe tratamiento para esta cita")
    return tratamiento