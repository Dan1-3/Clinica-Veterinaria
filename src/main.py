# Archivo principal de la aplicación FastAPI.
# Aquí se crea la app y se conectan las rutas de cada módulo (animales, propietarios, etc.).

from fastapi import FastAPI
from src.routes import animales_routes, propietarios_routes, veterinarios_routes, citas_routes, tratamientos_routes

app = FastAPI(title="Clínica Veterinaria API")

app.include_router(animales_routes.router)
app.include_router(propietarios_routes.router)
app.include_router(veterinarios_routes.router)
app.include_router(citas_routes.router)
app.include_router(tratamientos_routes.router)
