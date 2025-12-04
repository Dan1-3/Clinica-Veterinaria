from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from src.db.database import get_db
from src.schemas.cita_schema import CitaCreate, CitaRead
from src.services.citas_service import CitasService

router = APIRouter(prefix="/citas", tags=["Citas"])
service = CitasService()  # Instanciamos la clase del servicio, para usar sus métodos

# 1. Endpoint CREAR (POST)
@router.post("/", response_model=CitaRead)
def crear_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    return service.crear_cita(db, cita)

# 2. Endpoint LISTAR TODOS (GET)
@router.get("/", response_model=List[CitaRead])
def listar_citas(db: Session = Depends(get_db)):
    return service.listar_citas(db)

# 3. Endpoint BUSCAR POR ANIMAL (GET)
@router.get("/animal/{animal_id}", response_model=List[CitaRead])
def buscar_citas_por_animal(animal_id: int, db: Session = Depends(get_db)):
    # Esta ruta permite obtener el historial de un animal concreto
    return service.buscar_por_animal(db, animal_id)

# 4. Endpoint OBTENER UNO (GET)
@router.get("/{cita_id}", response_model=CitaRead)
def obtener_cita(cita_id: int, db: Session = Depends(get_db)):
    cita = service.obtener_cita(db, cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita

# 5. Endpoint ACTUALIZAR ESTADO (PUT) --> permite cambiar el estado de una cita (pendiente, completada, cancelada)
@router.put("/{cita_id}/estado", response_model=CitaRead)
def actualizar_estado(cita_id: int, nuevo_estado: str = Query(...), db: Session = Depends(get_db)):
    cita = service.actualizar_estado(db, cita_id, nuevo_estado)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita

# 6. Endpoint ELIMINAR (DELETE)
@router.delete("/{cita_id}")
def eliminar_cita(cita_id: int, db: Session = Depends(get_db)):
    exito = service.eliminar_cita(db, cita_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return {"message": "Cita eliminada correctamente"}