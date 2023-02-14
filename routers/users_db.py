from fastapi import APIRouter, HTTPException, Request, Depends
from db.models.user import Usuario
from db.client import db_client
from db.schemas.user import user_schema_secure, user_schema, users_schema
from bson import ObjectId
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

route = APIRouter(prefix="/userdb", tags=["userdb"])

templates = Jinja2Templates(directory="templates")

@route.get("/")
async def user_home():
    return RedirectResponse("/userdb/list")

@route.get("/list", response_class=HTMLResponse)
async def users_list (request: Request):
    users = users_schema(list(db_client.user.find()))
    return templates.TemplateResponse("views/user/user.html",{"request": request, "users": users})

# Path
@route.get("/search/{id}")
async def user_by_id (id: str):
    return buscar_usuario_por_columna("_id", ObjectId(id))

# Get - Create Form
@route.get("/formcreate")
async def form_create(request: Request):
    return templates.TemplateResponse("views/user/create.html",{"request": request})

# Get - Update Form
@route.get("/formupdate/{id}")
async def form_update(id: str, request: Request):
    user = user_schema_secure(db_client.user.find_one({"_id": ObjectId(id)}))
    return templates.TemplateResponse("views/user/update.html",{"request":request, "user": user})

# Post - Crear
@route.post("/create/", status_code=201)
async def create_user (user: Usuario = Depends(Usuario.as_form)):
    if type(buscar_usuario_por_columna(field="email", key=user.email)) == Usuario:
        raise HTTPException(status_code=404, detail="El usuario ya existe")

    user_dict = dict(user)

    id = db_client.user.insert_one(user_dict).inserted_id

    new_usuario = user_schema(db_client.user.find_one({"_id":id}))

    return RedirectResponse("/userdb", status_code=303)

# Post - Actualizar
@route.post("/update")
async def update_user (user: Usuario = Depends(Usuario.as_form_update)):
    
    user_dict = dict(user)
    password = user_schema(db_client.user.find_one({"_id": ObjectId(user.id)}))["password"]
    user_dict["password"] = password
    del user_dict["id"]

    try:
        db_client.user.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict)
    except:
        return {"error":"No se pudo actualizar el usuario"}
    
    return RedirectResponse("/userdb", status_code=303)

# Active / Inactive
@route.get("/changestate/{id}", status_code=204)
async def toggle_state(id: str):
    user = user_schema(db_client.user.find_one({"_id":ObjectId(id)}))
    print(user)

    if user["state"] :
        user["state"] = False
        db_client.user.find_one_and_replace({"_id":ObjectId(id)}, user)
    else:
        user["state"] = True
        db_client.user.find_one_and_replace({"_id":ObjectId(id)}, user)

    return RedirectResponse("/userdb/list")

# Delete - Eliminar
@route.delete("/delete/{id}", status_code=204)
async def delete_user (id: str):

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