# Aquí se definirán las clases (modelos) que representan las tablas de la base de datos.
# Cada clase será una entidad: Propietario, Animal, Veterinario, Cita, Tratamiento.

# Importamos las librerías necesarias de SQLAlchemy para definir los modelos
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text # campos básicos y claves foráneas
from sqlalchemy.orm import relationship # definir relaciones entre tablas
from src.db.database import Base # Importamos la clase Base desde database.py
import datetime 

# Definimos las clases (modelos) que representan las tablas de la base de datos
# Todas heredan de Base, definida en database.py

# 1. Tabla Propietarios
class Propietario(Base):
    __tablename__ = "propietarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    telefono = Column(String)
    direccion = Column(String)
    # Relación: Un dueño tiene muchas mascotas
    animales = relationship("Animal", back_populates="propietario", cascade="all, delete-orphan") # Cuando se borra un propietario, se borran sus animales también, pero no todos los registrados
# 2. Tabla Animales
class Animal(Base):
    __tablename__ = "animales"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    especie = Column(String)
    raza = Column(String)
    edad = Column(Integer)
    propietario_id = Column(Integer, ForeignKey("propietarios.id"))
    # Relaciones: pertenece a un dueño y tiene muchas citas
    propietario = relationship("Propietario", back_populates="animales")
    citas = relationship("Cita", back_populates="animal")

# 3. Tabla Veterinarios
class Veterinario(Base):
    __tablename__ = "veterinarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellidos = Column(String)   
    correo = Column(String, unique=True) 
    telefono = Column(String)
    horario = Column(String)      
    cargo = Column(String)
    # Relaciones: Un veterinario puede tener muchas citas
    citas = relationship("Cita", back_populates="veterinario")

# 4. Tabla Citas
class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc)) # Fecha y hora de la cita, lo definimos con zona horaria UTC
    motivo = Column(String)
    estado = Column(String, default="Pendiente")

    # Claves foráneas: referencias a otras tablas
    animal_id = Column(Integer, ForeignKey("animales.id"))
    veterinario_id = Column(Integer, ForeignKey("veterinarios.id"))
    propietario_id = Column(Integer, ForeignKey("propietarios.id"))

    # Relaciones: una cita pertenece a un animal, un veterinario y puede tener un tratamiento
    animal = relationship("Animal", back_populates="citas")
    veterinario = relationship("Veterinario", back_populates="citas")
    tratamiento = relationship("Tratamiento", back_populates="cita", uselist=False)

# 5. Tabla Tratamientos
class Tratamiento(Base):
    __tablename__ = "tratamientos"
    id = Column(Integer, primary_key=True, index=True)
    diagnostico = Column(Text)
    descripcion = Column(Text)
    cita_id = Column(Integer, ForeignKey("citas.id"), unique=True)
    # Relación: un tratamiento pertenece a una cita
    cita = relationship("Cita", back_populates="tratamiento")