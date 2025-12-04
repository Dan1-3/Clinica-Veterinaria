from sqlalchemy.orm import Session
from src.db.models import Veterinario
from src.schemas.veterinario_schema import VeterinarioCreate

class VeterinariosService:
    
    # 1. CREAR (POST)
    @staticmethod
    def crear_veterinario(db: Session, datos: VeterinarioCreate):
        # Creamos el objeto con los datos del esquema (schemas/veterinario_schema.py)
        nuevo_vet = Veterinario(
            nombre=datos.nombre,
            apellidos=datos.apellidos,
            correo=datos.correo,
            telefono=datos.telefono,
            horario=datos.horario,
            cargo=datos.cargo
        )
        # Guardamos en la base de datos
        db.add(nuevo_vet)
        db.commit()
        db.refresh(nuevo_vet)
        return nuevo_vet

    # 2. LISTAR TODOS (GET)
    @staticmethod
    def listar_veterinarios(db: Session):
        return db.query(Veterinario).all()

    # 3. OBTENER UNO (GET por ID)
    @staticmethod
    def obtener_veterinario(db: Session, veterinario_id: int):
        return db.query(Veterinario).filter(Veterinario.id == veterinario_id).first()

    # 4. ACTUALIZAR (PUT)
    @staticmethod
    def actualizar_veterinario(db: Session, veterinario_id: int, nuevos_datos: VeterinarioCreate):
        # Buscamos al veterinario por su ID, para luego actualizar sus datos
        vet = db.query(Veterinario).filter(Veterinario.id == veterinario_id).first()
        
        if vet:
            # Actualizamos campo a campo
            vet.nombre = nuevos_datos.nombre
            vet.apellidos = nuevos_datos.apellidos
            vet.correo = nuevos_datos.correo
            vet.telefono = nuevos_datos.telefono
            vet.horario = nuevos_datos.horario
            vet.cargo = nuevos_datos.cargo
            
            db.commit()
            db.refresh(vet)
        return vet

    # 5. ELIMINAR (DELETE)
    @staticmethod
    def eliminar_veterinario(db: Session, veterinario_id: int):
        vet = db.query(Veterinario).filter(Veterinario.id == veterinario_id).first()
        if vet:
            db.delete(vet)
            db.commit()
            return True
        return False