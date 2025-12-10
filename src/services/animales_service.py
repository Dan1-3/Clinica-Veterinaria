# Aquí se programarán las funciones que gestionan la lógica de los animales
# Por ejemplo: crear, consultar, listar, actualizar y eliminar animales.

from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.db.models import Animal, Cita, Tratamiento, Propietario 
from src.schemas.animal_schema import AnimalCreate

class AnimalesService:
    
    # 1. CREAR: se encarga de crear un nuevo animal en la base de datos, recibiendo los datos necesarios que cumplen con el esquema AnimalCreate de schemas/animal_schema.py
    @staticmethod
    def crear_animal(db: Session, animal: AnimalCreate):
        nuevo_animal = Animal(
            nombre=animal.nombre,
            especie=animal.especie,
            raza=animal.raza,
            edad=animal.edad,
            propietario_id=animal.propietario_id
        )
        db.add(nuevo_animal) # Agregamos el nuevo animal a la sesión
        db.commit() # Guardamos los cambios en la base de datos
        db.refresh(nuevo_animal) # Refrescamos la instancia para obtener el ID generado
        return nuevo_animal 

    # 2. LISTAR TODOS: devuelve una lista con todos los animales en la base de datos
    @staticmethod
    def listar_animales(db: Session):
        return db.query(Animal).all()

    # 3. OBTENER UNO: busca un animal por su ID y lo devuelve si existe
    @staticmethod
    def obtener_animal(db: Session, animal_id: int):
        return db.query(Animal).filter(Animal.id == animal_id).first()
    
    # 4. ACTUALIZAR: actualiza los datos de un animal existente por su ID
    @staticmethod
    def actualizar_animal(db: Session, animal_id: int, animal: AnimalCreate):
        # 1. Buscamos el animal existente
        db_animal = db.query(Animal).filter(Animal.id == animal_id).first()
        
        if not db_animal:
            raise HTTPException(status_code=404, detail="Animal no encontrado")
        
        # 2. Actualizamos sus datos campo a campo
        db_animal.nombre = animal.nombre
        db_animal.especie = animal.especie
        db_animal.raza = animal.raza
        db_animal.edad = animal.edad
        db_animal.propietario_id = animal.propietario_id
        
        # 3. Guardamos cambios
        db.commit()
        db.refresh(db_animal)
        return db_animal

    # 5. ELIMINAR: elimina un animal por su ID si existe
    @staticmethod
    def eliminar_animal(db: Session, animal_id: int):
        animal = db.query(Animal).filter(Animal.id == animal_id).first()
        if animal:
            db.delete(animal)
            db.commit()
            return True
        return False
    
    # 6. FICHA CLINICA COMPLETA DEL ANIMAL
    @staticmethod
    def obtener_ficha_clinica(db: Session, animal_id: int):
        # 1. Buscar Animal
        animal = db.query(Animal).filter(Animal.id == animal_id).first() # buscar el animal por su ID .first para obtener uno solo (el primero que encuentre)
        if not animal: return None
        
        # 2. Buscar Nombre del Dueño (para mostrarlo en la ficha)
        prop = db.query(Propietario).filter(Propietario.id == animal.propietario_id).first()
        nombre_prop = prop.nombre if prop else "Desconocido"
        
        # 3. Buscar Citas (Ordenadas por fecha, la más reciente primero)
        citas = db.query(Cita).filter(Cita.animal_id == animal.id).order_by(Cita.fecha_hora.desc()).all() # obtener todas las citas del animal, ordenadas por fecha descendente
        
        lista_citas = []
        for c in citas:
            # 4. Por cada cita, buscar si tiene tratamiento/diagnóstico
            trat = db.query(Tratamiento).filter(Tratamiento.cita_id == c.id).first()
            
            # Crear diccionario de la cita con el tratamiento anidado
            datos_cita = {
                "id": c.id,
                "fecha_hora": c.fecha_hora,
                "motivo": c.motivo,
                "estado": c.estado,
                "veterinario_id": c.veterinario_id,
                "tratamiento": trat # SQLAlchemy pasa el objeto, Pydantic lo filtra
            }
            lista_citas.append(datos_cita)

        # 5. Retornar estructura completa
        return {
            "id": animal.id,
            "nombre": animal.nombre,
            "especie": animal.especie,
            "raza": animal.raza,
            "edad": animal.edad,
            "propietario_id": animal.propietario_id,
            "propietario_nombre": nombre_prop,
            "citas": lista_citas
        }