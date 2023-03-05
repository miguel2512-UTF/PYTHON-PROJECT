from fastapi import FastAPI, Request, Depends
from routers import products, users, users_db, login, home
from fastapi.staticfiles import StaticFiles
from routers.login import current_user, is_admin
from config.settings import Settings as settings
from security.config import SecurityConfig as security
from starlette.middleware.sessions import SessionMiddleware
from config.exception_handler import exception

app = FastAPI(exception_handlers=exception)

app.add_middleware(SessionMiddleware, secret_key=security.SECRET)

templates = settings.TEMPLATES

IS_AUTHENTICATED = [Depends(current_user)]
IS_ADMIN = [Depends(is_admin)]

# Routers
app.include_router(products.route, dependencies=IS_AUTHENTICATED)
app.include_router(users.route)
app.include_router(users_db.route, dependencies=IS_ADMIN)
app.include_router(login.route)
app.include_router(home.route, dependencies=IS_AUTHENTICATED)
app.mount("/static", StaticFiles(directory = "static"), name="static")

@app.get("/")
async def root (request: Request):
    #return "Hola mundo!!!!"
    return templates.TemplateResponse("views/index.html",{"request": request, "message":"Hola mundo!"})

@app.get("/url")
async def url ():
    return {"url" : "www.youtube.com"}

# Documentación con Swagger: 127.0.0.1:8000/docs
# Documentación con Redocly: 127.0.0.1:8000/redoc
