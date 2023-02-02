from fastapi import APIRouter, HTTPException
from db.models.user import Usuario
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

route = APIRouter(prefix="/userdb", tags=["userdb"])

@route.get("/listar", response_model=list[Usuario])
async def users ():
    return users_schema(list(db_client.user.find()))

# Path
@route.get("/buscar/{id}")
async def user_by_id (id: str):
    return buscar_usuario_por_columna("_id", ObjectId(id))

# Post - Crear
@route.post("/crear/", response_model=Usuario, status_code=201)
async def crear_usuario (user: Usuario):
    if type(buscar_usuario_por_columna(field="email", key=user.email)) == Usuario:
        raise HTTPException(status_code=404, detail="El usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.user.insert_one(user_dict).inserted_id

    new_usuario = user_schema(db_client.user.find_one({"_id":id}))

    return Usuario(**new_usuario)

# Put - Actualizar
@route.put("/actualizar")
async def actualizar_usuario (user: Usuario):
    
    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.user.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict)
    except:
        return {"error":"No se pudo actualizar el usuario"}
    
    return buscar_usuario_por_columna("_id",ObjectId(user.id))

# Delete - Eliminar
@route.delete("/delete/{id}", status_code=204)
async def eliminar_usuario (id: str):

    found = db_client.user.find_one_and_delete({"_id":ObjectId(id)})

    if not found:
        return {"error":"El usuario no pudo ser eliminado"}
    
    return {"message":"usuario eliminado exitosamente"}

def buscar_usuario_por_columna (field: str, key):

    try:
        user = db_client.user.find_one({field:key})
        return Usuario(**user_schema(user))
    except:
        return {"error" : "No se ha encontrado el usuario"}