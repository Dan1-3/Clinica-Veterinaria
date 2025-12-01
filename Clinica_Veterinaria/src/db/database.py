# Aquí se establecerá la conexión con la base de datos (SQLite).
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Configuración de SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./clinica.db"

# 2. Creamos el motor de la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Creamos la sesión (para poder guardar/leer datos)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Clase Base para los modelos
Base = declarative_base()

# 5. ESTA ES LA FUNCIÓN QUE TE FALTA (get_db)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()