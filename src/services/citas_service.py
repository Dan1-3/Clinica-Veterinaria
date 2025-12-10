from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.db.models import Cita, Veterinario, Animal
from src.schemas.cita_schema import CitaCreate

class CitasService:
    
    # 1. CREAR CITA
    @staticmethod
    def crear_cita(db: Session, cita_data: CitaCreate):
        if not db.query(Animal).filter(Animal.id == cita_data.animal_id).first():
            raise HTTPException(status_code=404, detail="El Animal no existe")
            
        if not db.query(Veterinario).filter(Veterinario.id == cita_data.veterinario_id).first():
            raise HTTPException(status_code=404, detail="El Veterinario no existe")
        
        nueva_cita = Cita(
            fecha_hora=cita_data.fecha_hora,
            motivo=cita_data.motivo,
            estado=cita_data.estado,
            animal_id=cita_data.animal_id,
            propietario_id=cita_data.propietario_id,
            veterinario_id=cita_data.veterinario_id
        )
        db.add(nueva_cita)
        db.commit()
        db.refresh(nueva_cita)
        return nueva_cita

    # 2. OBTENER UNA CITA POR ID
    def obtener_cita(self, db: Session, cita_id: int):
        return db.query(Cita).filter(Cita.id == cita_id).first()

    # 3. LISTAR TODAS
    def listar_citas(self, db: Session):
        return db.query(Cita).all()

    # 4. ACTUALIZAR ESTADO (Ej: de "Pendiente" a "Realizada")
    def actualizar_estado(self, db: Session, cita_id: int, nuevo_estado: str):
        cita = self.obtener_cita(db, cita_id)
        if cita:
            cita.estado = nuevo_estado
            db.commit()
            db.refresh(cita)
            return cita
        return None

    # 5. ELIMINAR CITA
    def eliminar_cita(self, db: Session, cita_id: int):
        cita = self.obtener_cita(db, cita_id)
        if cita:
            db.delete(cita)
            db.commit()
            return True
        return False

    # 6. BUSCAR CITAS DE UN ANIMAL ESPECÍFICO
    def buscar_por_animal(self, db: Session, animal_id: int):
        return db.query(Cita).filter(Cita.animal_id == animal_id).all()