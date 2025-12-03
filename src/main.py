# Archivo principal de la aplicación FastAPI.
# Aquí se crea la app y se conectan las rutas de cada módulo (animales, propietarios, etc.).

from fastapi import FastAPI
from src.db.database import Base, engine
# Importamos las rutas
from src.routes import propietarios_routes, animales_routes, veterinarios_routes, citas_routes
from src.routes import tratamientos_routes

#Si no existen las tablas, se crean
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clínica Veterinaria API")

# Incluir los routers
app.include_router(propietarios_routes.router)
app.include_router(animales_routes.router)
app.include_router(veterinarios_routes.router)
app.include_router(citas_routes.router)
app.include_router(tratamientos_routes.router)