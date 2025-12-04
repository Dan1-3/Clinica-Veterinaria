# Aqui se programarán las funciones que gestionan la lógica de los propietarios.
# Importamos logging para registrar eventos importantes y errores.

import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from src.db.models import Propietario
from src.schemas.propietario_schema import PropietarioCreate
from src.utils.validators import EmailValidator, TelefonoValidator

# Configuramos el logger: el nivel minimo mostrado es INFO, y el formato incluye fecha, nivel y mensaje
# Los logging los podemos ver en la consola al ejecutar la aplicacion
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s") 
logger = logging.getLogger(__name__)

class PropietariosService:
    
    @staticmethod
    def crear_propietario(db: Session, propietario_data: PropietarioCreate):
        
        # 1. VALIDACIONES DE CAMPOS OBLIGATORIOS: comprobar que no esten vacios (nombre, direccion)
        if not propietario_data.nombre or not propietario_data.nombre.strip(): #strip para evitar solo espacios
            raise HTTPException(status_code=400, detail="El nombre es obligatorio y no puede estar vacío.")
            
        if not propietario_data.direccion or not propietario_data.direccion.strip():
            raise HTTPException(status_code=400, detail="La dirección es obligatoria.")

        # 2. VALIDACIONES ESPECIFICAS DE FORMATO: EMAIL Y TELEFONO --> definidos en utils/validators.py
        if not EmailValidator.validar(propietario_data.email):
            logger.warning(f"Email inválido: {propietario_data.email}")
            raise HTTPException(status_code=400, detail="El formato del correo no es válido.")
            
        if not TelefonoValidator.validar(propietario_data.telefono):
            logger.warning(f"Teléfono inválido: {propietario_data.telefono}")
            raise HTTPException(status_code=400, detail="El teléfono debe empezar por 6 y tener 9 dígitos.")

        # 3. CREACION DEL PROPIETARIO: si pasa las validaciones, intentamos crear el registro en la BD
        try:
            nuevo_propietario = Propietario(
                nombre=propietario_data.nombre.strip(), 
                email=propietario_data.email.strip(),
                telefono=propietario_data.telefono.strip(),
                direccion=propietario_data.direccion.strip()
            )
            db.add(nuevo_propietario)
            db.commit()
            db.refresh(nuevo_propietario)
            
            # 4. LOGGING DE EXITO: registramos la creacion exitosa
            logger.info(f"Propietario creado: ID {nuevo_propietario.id}")
            return nuevo_propietario

        # 5. MANEJO DE ERRORES: capturamos errores comunes como duplicados o fallos inesperados
        except IntegrityError as e:
            db.rollback() # revertimos la transaccion en caso de error
            logger.error(f"Duplicado: {e}")
            raise HTTPException(status_code=409, detail="Ya existe un propietario con ese correo electrónico.")
            
        except Exception as e:
            db.rollback()
            logger.critical(f"Error inesperado: {e}")
            raise HTTPException(status_code=500, detail="Error interno del servidor.")

    @staticmethod
    def listar_propietarios(db: Session):
        return db.query(Propietario).all()

    @staticmethod
    def obtener_propietario(db: Session, propietario_id: int):
        return db.query(Propietario).filter(Propietario.id == propietario_id).first()

    @staticmethod
    def actualizar_propietario(db: Session, propietario_id: int, nuevos_datos: PropietarioCreate):
        propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
        if propietario:
            # Validaciones también al actualizar
            if not TelefonoValidator.validar(nuevos_datos.telefono):
                raise HTTPException(status_code=400, detail="El teléfono debe empezar por 6.")
                
            propietario.nombre = nuevos_datos.nombre
            propietario.email = nuevos_datos.email
            propietario.telefono = nuevos_datos.telefono
            propietario.direccion = nuevos_datos.direccion
            db.commit()
            db.refresh(propietario)
        return propietario

    @staticmethod
    def eliminar_propietario(db: Session, propietario_id: int):
        propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
        if propietario:
            db.delete(propietario)
            db.commit()
            return True
        return False