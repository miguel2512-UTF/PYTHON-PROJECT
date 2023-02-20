from pydantic import BaseModel
from typing import Optional
from fastapi import Form, Request
from db.models.validation import is_valid
from config import messages

NAME_REGEXP=r"[A-Za-zÀ-ÿ]{2,10}[\s]{0,1}[A-Za-zÀ-ÿ]{2,10}"
EMAIL_REGEXP=r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})"
PASSWROD_REGEXP=r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
        
# Entidad Usuario
class Usuario(BaseModel):
    id: Optional[str]
    name: str
    email: str
    password: Optional[str]
    role: str
    state: bool
    
    async def as_form(
        request: Request 
    ):
        form = await request.form()
        id = form.get("id")
        name = form.get("name")
        email = form.get("email")
        password = form.get("password")
        role = form.get("role")
        state = form.get("state")
        if len(state)==0 or state.lower()=="true":
            state=True
        else:
            state=False

        return Usuario(
            id=id,
            name=name,
            email=email,
            password=password,
            role=role,
            state=state
        )
    
    def is_valid_user(user, action: str):
        error={}
        if len(user.name)==0:
            error["name"]=messages.msg_field_required("name")
        elif not is_valid(NAME_REGEXP, user.name):
            error["name"]=messages.MSG_USER_NAME
        if len(user.email)==0:
            error["email"]=messages.msg_field_required("email")
        elif not is_valid(EMAIL_REGEXP, user.email):
            error["email"]=messages.MSG_USER_EMAIL
        if not action == "update":
            if len(user.password)==0:
                error["password"]=messages.msg_field_required("password")
            elif not is_valid(PASSWROD_REGEXP, user.password):
                error["password"]=messages.MSG_USER_PASSWORD
        if len(user.role)==0:
            error["role"]=messages.msg_field_required("role")
        elif not user.role == "admin" and not user.role == "user":
            error["role"]=messages.MSG_USER_ROLE

        return error