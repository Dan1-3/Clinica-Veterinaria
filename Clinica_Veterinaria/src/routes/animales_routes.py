# Aquí se definirán los endpoints (rutas) de la API relacionados con animales.
# Cada ruta conectará con las funciones del servicio para manejar las peticiones.

from fastapi import APIRouter

router = APIRouter(prefix="/animales", tags=["Animales"])

@router.post("/")
def crear_animal():
    pass

@router.get("/")
def listar_animales():
    pass

@router.get("/{animal_id}")
def obtener_animal(animal_id: int):
    pass

@router.put("/{animal_id}")
def actualizar_animal(animal_id: int):
    pass

@router.delete("/{animal_id}")
def eliminar_animal(animal_id: int):
    pass
