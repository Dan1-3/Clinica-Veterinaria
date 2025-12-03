from sqlalchemy.orm import Session
from src.db.models import Propietario
from src.schemas.propietario_schema import PropietarioCreate

class PropietariosService:
    
    # 1. CREAR
    @staticmethod
    def crear_propietario(db: Session, propietario_data: PropietarioCreate):
        nuevo_propietario = Propietario(
            nombre=propietario_data.nombre,
            email=propietario_data.email,
            telefono=propietario_data.telefono,
            direccion=propietario_data.direccion
        )
        db.add(nuevo_propietario)
        db.commit()
        db.refresh(nuevo_propietario)
        return nuevo_propietario

    # 2. LISTAR TODOS
    @staticmethod
    def listar_propietarios(db: Session):
        return db.query(Propietario).all()

    # 3. OBTENER UNO POR ID
    @staticmethod
    def obtener_propietario(db: Session, propietario_id: int):
        return db.query(Propietario).filter(Propietario.id == propietario_id).first()

    # 4. ACTUALIZAR
    @staticmethod
    def actualizar_propietario(db: Session, propietario_id: int, nuevos_datos: PropietarioCreate):
        propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
        if propietario:
            propietario.nombre = nuevos_datos.nombre
            propietario.email = nuevos_datos.email
            propietario.telefono = nuevos_datos.telefono
            propietario.direccion = nuevos_datos.direccion
            db.commit()
            db.refresh(propietario)
        return propietario

    # 5. ELIMINAR
    @staticmethod
    def eliminar_propietario(db: Session, propietario_id: int):
        propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
        if propietario:
            db.delete(propietario)
            db.commit()
            return True
        return False