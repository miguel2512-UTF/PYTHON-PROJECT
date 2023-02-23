from fastapi import Request, HTTPException, status
from config.settings import Settings

templates = Settings.TEMPLATES

async def not_found(request: Request, exc: HTTPException):
    return templates.TemplateResponse("views/error/404.html",{"request": request}, status_code=status.HTTP_404_NOT_FOUND)

async def forbidden(request: Request, exc: HTTPException):
    return templates.TemplateResponse("views/error/403.html",{"request": request}, status_code=status.HTTP_403_FORBIDDEN)

async def internal_server_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse("views/error/500.html",{"request": request}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

async def inactive_user(request: Request, exc: HTTPException):
    return templates.TemplateResponse("views/error/inactive.html",{"request": request}, status_code=status.HTTP_423_LOCKED)

exception = {
    404: not_found,
    403: forbidden,
    500: internal_server_error,
    423: inactive_user
}