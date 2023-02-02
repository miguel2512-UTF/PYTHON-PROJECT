from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITMO = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

crypt = CryptContext(schemes=["bcrypt"])

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
        "password":"$2a$12$KI4Ye/WPGMXsjfhFea8TEOFL48bwnLITr/30qvEcBMWrVBwTo1HnK"
    },
    "carlos3023":{
        "id": 1,
        "username":"carlos3023",
        "nombre_completo":"Carlos Gonzales 2",
        "email":"carlos@gmail.com",
        "estado": False,
        "password":"$2a$12$cP2VNsDrbR1UgprT380w3eFOxZ/U.m7iF18Q9gOIuk/hI288ipG92"
    }
}

def buscar_usuario_db (username: str):
    if username in users_db:
        return UsuarioDB(**users_db[username])

def buscar_usuario (username: str):
    if username in users_db:
        return Usuario(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(status_code=401, 
            detail="Credenciales inválidas", 
            headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITMO).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return buscar_usuario(username)

async def current_user (user: Usuario = Depends(auth_user)):

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

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {"sub":user.username, "exp": expire}
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITMO), "tolen_type": "bearer"}

@app.get("/users/me")
async def users_me (user: Usuario = Depends(current_user)):
    return user