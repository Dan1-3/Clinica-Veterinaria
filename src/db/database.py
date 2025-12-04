# Aquí se establecerá la conexión con la base de datos (SQLite).
from sqlalchemy import create_engine  # Importamos create_engine para crear la conexión con la base de datos
from sqlalchemy.ext.declarative import declarative_base #Importamos declarative_base para definir la clase base de los modelos
from sqlalchemy.orm import sessionmaker # Importamos sessionmaker para crear sesiones de base de datos

# 1. Configuración de SQLite, la URL de la base de datos
SQLALCHEMY_DATABASE_URL = "sqlite:///./clinica.db"

# 2. Creamos el motor de la base de datos, para conectarnos a SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Creamos la sesión (para poder guardar/leer datos), vinculada al motor
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Clase Base para los modelos, que heredan de ella
Base = declarative_base()

# 5. Dependencia para obtener la sesión de la base de datos, usada en FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()