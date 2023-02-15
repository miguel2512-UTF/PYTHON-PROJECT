from fastapi import FastAPI, Request, Depends
from routers import products, users, users_db, login, home
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers.login import current_user

app = FastAPI()

templates = Jinja2Templates(directory="templates")

PROTECT = [Depends(current_user)]

# Routers
app.include_router(products.route)
app.include_router(users.route)
app.include_router(users_db.route, dependencies=PROTECT)
app.include_router(login.route)
app.include_router(home.route, dependencies=PROTECT)
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
