from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

route = APIRouter()

# Entidad Usuario
class Usuario(BaseModel):
    id: int
    nombre: str
    apellido: str
    edad: int

# Datos quemados
usuarios_list = [
    Usuario(id=1,nombre="miguel",apellido="wilchez",edad=18),
    Usuario(id=2,nombre="camila",apellido="wilchez",edad=17),
    Usuario(id=3,nombre="marvin",apellido="donado",edad=23)]

@route.get("/usersjson")
async def usersjson ():
    return [
        {"nombre":"miguel", "apellido":"wilchez","edad":18},
        {"nombre":"camila", "apellido":"wilchez","edad":17},
        {"nombre":"marvin", "apellido":"donado","edad":23}
        ]

@route.get("/users")
async def users ():
    return usuarios_list

# Path
@route.get("/user/{id}")
async def user_by_id (id: int):
    return buscar_usuario(id)

# Query
@route.get("/userquery/")
async def user_by_id (id: int):
    return buscar_usuario(id)

# Post - Crear
@route.post("/user/", response_model=Usuario, status_code=201)
async def crear_usuario (user: Usuario):
    if type(buscar_usuario(user.id)) == Usuario:
        raise HTTPException(status_code=204, detail="El usuario ya existe")
    else:
        usuarios_list.append(user)
        return user

# Put - Actualizar
@route.put("/user/")
async def actualizar_usuario (user: Usuario):
    
    found = False
    for index, saved_user in enumerate(usuarios_list):
        if saved_user.id == user.id:
            usuarios_list[index] = user
            found = True
    
    if not found:
        return {"error":"Usuario no encontrado"}
    
    return user

# Delete - Eliminar
@route.delete("/user/{id}")
async def eliminar_usuario (id: int):

    found = False

    for index, user in enumerate(usuarios_list):
        if user.id == id:
            del usuarios_list[index]
            found = True

    if not found:
        return {"error":"El usuario no pudo ser eliminado"}
    
    return {"message":"usuario eliminado exitosamente"}

def buscar_usuario (id: int):
    usuarios = filter(lambda usuario: usuario.id == id, usuarios_list)
    try:
        return list(usuarios)[0]
    except:
        return {"error" : "No se ha encontrado el usuario"}