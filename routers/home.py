from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from routers.login import current_user

route = APIRouter()

templates = Jinja2Templates(directory="templates")

@route.get("/home")
async def home(request: Request, auth = Depends(current_user)):
    return templates.TemplateResponse("views/principal.html",{"request":request})
