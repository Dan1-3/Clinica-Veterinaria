from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.db.database import get_db
from src.schemas.veterinario_schema import VeterinarioCreate, VeterinarioRead
from src.services.veterinarios_service import VeterinariosService

router = APIRouter(prefix="/veterinarios", tags=["Veterinarios"])

# Instanciamos el servicio (o usamos métodos estáticos directamente)
service = VeterinariosService()

@router.post("/", response_model=VeterinarioRead)
def crear_veterinario(vet: VeterinarioCreate, db: Session = Depends(get_db)):
    return service.crear_veterinario(db, vet)

@router.get("/", response_model=List[VeterinarioRead])
def listar_veterinarios(db: Session = Depends(get_db)):
    return service.listar_veterinarios(db)

@router.get("/{vet_id}", response_model=VeterinarioRead)
def obtener_veterinario(vet_id: int, db: Session = Depends(get_db)):
    vet = service.obtener_veterinario(db, vet_id)
    if not vet:
        raise HTTPException(status_code=404, detail="Veterinario no encontrado")
    return vet

@router.put("/{vet_id}", response_model=VeterinarioRead)
def actualizar_veterinario(vet_id: int, vet_data: VeterinarioCreate, db: Session = Depends(get_db)):
    vet = service.actualizar_veterinario(db, vet_id, vet_data)
    if not vet:
        raise HTTPException(status_code=404, detail="Veterinario no encontrado")
    return vet

@router.delete("/{vet_id}")
def eliminar_veterinario(vet_id: int, db: Session = Depends(get_db)):
    exito = service.eliminar_veterinario(db, vet_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Veterinario no encontrado")
    return {"message": "Veterinario eliminado correctamente"}