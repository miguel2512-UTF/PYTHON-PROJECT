from fastapi import APIRouter

route = APIRouter(prefix="/productos",tags=["products"], responses={404: {"message":"No encontrado"}})

productos_lista = [
    "Producto 1",
    "Producto 2",
    "Producto 3",
    "Producto 4"
]

@route.get("/listar")
async def productos ():
    return [
        "Producto 1",
        "Producto 2",
        "Producto 3",
        "Producto 4"
        ]

@route.get("/buscar/{id}")
async def productos (id: int):
    return productos_lista[id]