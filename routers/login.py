from fastapi import APIRouter, Request, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from db.client import db_client
from db.models.user import Usuario
from db.schemas.user import user_schema, user_schema_secure
from security.utils import OAuth2PasswordBearerWithCookie
from security.config import SecurityConfig as security
from config.settings import Settings as settings
from fastapi.responses import RedirectResponse

route = APIRouter()

templates = settings.TEMPLATES

crypt = CryptContext(schemes=["bcrypt"])

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl=security.URL_LOGIN)

@route.get("/login")
async def login_form (request: Request):
    return templates.TemplateResponse("views/login.html", {"request": request, "form": ""})

@route.post("/login")
async def login_post (response: Response, request: Request, form: OAuth2PasswordRequestForm = Depends()):
    email = form.username
    user_db = db_client.user.find_one({"email": email})
    if user_db:
        user = Usuario(**user_schema(user_db))

    if not user_db or not crypt.verify(form.password, user.password):
        return templates.TemplateResponse("views/login.html",{"request": request, "form": form, "error": "Wrong password or user"})

    expire = datetime.utcnow() + timedelta(hours=security.ACCESS_TOKEN_DURATION)

    request.session["user"] = user.name
    request.session["role"] = user.role

    access_token = {"sub":user.email, "exp": expire}
    response.set_cookie(key="access_token", value=f"Bearer {jwt.encode(access_token, security.SECRET, algorithm=security.ALGORITMO)}", httponly=True)

    response.status_code= 303
    response.headers["location"] = security.URL_SUCCESSFULLY_LOGIN

@route.get("/logout")
async def logout(response: Response, request: Request):
    response.delete_cookie("access_token")
    request.session.clear()

    response.status_code = 303
    response.headers["location"] = security.URL_LOGIN

async def auth_user(token: str = Depends(oauth2_scheme)):

    exception = HTTPException(
        status_code=303,
        detail="Not authenticated",
        headers={"location": security.URL_LOGIN},
    )

    try:
        username = jwt.decode(token, security.SECRET, algorithms=[security.ALGORITMO]).get("sub")
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