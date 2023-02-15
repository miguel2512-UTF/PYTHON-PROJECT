from fastapi import APIRouter, Request, HTTPException, Depends, Response
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from db.client import db_client
from db.models.user import Usuario
from db.schemas.user import user_schema, user_schema_secure
from security.utils import OAuth2PasswordBearerWithCookie
from security.config import Config

route = APIRouter()

templates = Jinja2Templates(directory="templates")

crypt = CryptContext(schemes=["bcrypt"])

oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

access_token=dict()

@route.get("/login")
async def login_form (request: Request):
    return templates.TemplateResponse("views/login.html", {"request": request})

@route.post("/login")
async def login_post (response: Response, form: OAuth2PasswordRequestForm = Depends()):
    user_db = db_client.user.find_one({"email": form.username})
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    
    user = Usuario(**user_schema(user_db))

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")

    expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_DURATION)
    print(expire)

    access_token = {"sub":user.email, "exp": expire}
    response.set_cookie(key="access_token", value=f"Bearer {jwt.encode(access_token, Config.SECRET, algorithm=Config.ALGORITMO)}", httponly=True)

    response.status_code= 303
    response.headers["location"] = "/userdb"

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login")

async def auth_user(token: str = Depends(oauth2_scheme)):

    exception = HTTPException(status_code=401, 
            detail="Credenciales inválidas", 
            headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, Config.SECRET, algorithms=[Config.ALGORITMO]).get("sub")
        print("email is", username)
        if username is None:
            raise exception

    except JWTError:
        raise exception

    user = db_client.user.find_one({"email": username})
    return Usuario(**user_schema_secure(user))

async def current_user (user: Usuario = Depends(auth_user)):

    if not user.state:
        raise HTTPException(status_code=400, 
            detail="Usuario no activo", 
            headers={"WWW-Authenticate": "Bearer"})

    return user

@route.get("/me")
async def me(user: Usuario = Depends(current_user)):
    return user