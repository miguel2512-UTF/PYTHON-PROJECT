from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

class Usuario(BaseModel):
    id: int
    username: str
    nombre_completo: str
    email: str
    estado: bool

class UsuarioDB(Usuario):
    password: str

users_db = {
    "miguel2512":{
        "id": 1,
        "username":"miguel2512",
        "nombre_completo":"Miguel Wilchez",
        "email":"miguel@gmail.com",
        "estado": True,
        "password":"1234"
    },
    "carlos3023":{
        "id": 1,
        "username":"carlos3023",
        "nombre_completo":"Carlos Gonzales 2",
        "email":"carlos@gmail.com",
        "estado": False,
        "password":"4321"
    }
}

async def current_user (token: str = Depends(oauth2)):
    user = buscar_usuario(token)
    if not user:
        raise HTTPException(status_code=401, 
            detail="Credenciales inválidas", 
            headers={"WWW-Authenticate": "Bearer"})

    if not user.estado:
        raise HTTPException(status_code=400, 
            detail="Usuario no activo", 
            headers={"WWW-Authenticate": "Bearer"})

    return user

@app.post("/login")
async def login (form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")

    user = buscar_usuario_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")

    return {"access_token": user.username, "tolen_type": "bearer"}

@app.get("/users/me")
async def users_me (user: Usuario = Depends(current_user)):
    return user

def buscar_usuario_db (username: str):
    if username in users_db:
        return UsuarioDB(**users_db[username])

def buscar_usuario (username: str):
    if username in users_db:
        return Usuario(**users_db[username])