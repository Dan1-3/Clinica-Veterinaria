# Aquí se definirán las clases (modelos) que representan las tablas de la base de datos.
# Cada clase será una entidad: Propietario, Animal, Veterinario, Cita, Tratamiento.

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from src.db.database import Base
import datetime

# 1. Tabla Propietarios
class Propietario(Base):
    __tablename__ = "propietarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    telefono = Column(String)
    direccion = Column(String)
    # Relación: Un dueño tiene muchas mascotas
    animales = relationship("Animal", back_populates="propietario")

# 2. Tabla Animales
class Animal(Base):
    __tablename__ = "animales"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    especie = Column(String)
    raza = Column(String)
    edad = Column(Integer)
    propietario_id = Column(Integer, ForeignKey("propietarios.id"))
    # Relaciones
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
    # Relaciones
    citas = relationship("Cita", back_populates="veterinario")

# 4. Tabla Citas
class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime, default=datetime.datetime.utcnow) # <--- CORREGIDO para usar 'fecha_hora'
    motivo = Column(String)
    estado = Column(String, default="Pendiente")

    # Claves foráneas
    animal_id = Column(Integer, ForeignKey("animales.id"))
    veterinario_id = Column(Integer, ForeignKey("veterinarios.id"))
    propietario_id = Column(Integer, ForeignKey("propietarios.id")) # <--- AÑADIDO: Clave foránea para evitar JOINs largos

    # Relaciones
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
    cita = relationship("Cita", back_populates="tratamiento")