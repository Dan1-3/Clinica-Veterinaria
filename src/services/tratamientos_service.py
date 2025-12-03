from sqlalchemy.orm import Session
from src.db.models import Tratamiento
from src.schemas.tratamiento_schema import TratamientoCreate

class TratamientosService:

    # 1. CREAR TRATAMIENTO
    @staticmethod
    def crear_tratamiento(db: Session, datos: TratamientoCreate):
        nuevo_tratamiento = Tratamiento(
            diagnostico=datos.diagnostico,
            descripcion=datos.descripcion,
            cita_id=datos.cita_id
        )
        db.add(nuevo_tratamiento)
        db.commit()
        db.refresh(nuevo_tratamiento)
        return nuevo_tratamiento

    # 2. OBTENER POR ID DE CITA (Para saber si una cita ya tiene diagnóstico)
    @staticmethod
    def obtener_por_cita(db: Session, cita_id: int):
        return db.query(Tratamiento).filter(Tratamiento.cita_id == cita_id).first()