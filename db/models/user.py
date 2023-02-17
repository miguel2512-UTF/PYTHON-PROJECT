from pydantic import BaseModel
from typing import Optional
from fastapi import Form
from db.models.validation import is_valid

NAME_REGEXP=r"[A-Za-zÀ-ÿ]{2,10}[\s]{0,1}[A-Za-zÀ-ÿ]{2,10}"
EMAIL_REGEXP=r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})"
PASSWROD_REGEXP=f"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
        
# Entidad Usuario
class Usuario(BaseModel):
    id: Optional[str]
    name: str
    email: str
    password: Optional[str]
    role: str
    state: bool
    
    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        role: str = Form(...),
        state: bool = Form(...)
    ):
        return cls(
            name = name,
            email = email,
            password = password,
            role = role,
            state = state
        )
    
    @classmethod
    def as_form_update(
        cls,
        id: str = Form(...),
        name: str = Form(...),
        email: str = Form(...),
        role: str = Form(...),
        state: bool = Form(...)
    ):
        return cls(
            id = id,
            name = name,
            email = email,
            role = role,
            state = state
        )
    
    def is_valid_user(user):
        error={}
        if not is_valid(NAME_REGEXP, user.name):
            error["name"]="Wrong name"
        if not is_valid(EMAIL_REGEXP, user.email):
            error["email"]="Wrong email"
        if not is_valid(PASSWROD_REGEXP, user.password):
            error["password"]="Wrong password"
        if not user.role == "admin" and not user.role == "user":
            error["role"]="Wrong role"

        return error