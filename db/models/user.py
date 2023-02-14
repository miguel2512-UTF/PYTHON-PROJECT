from pydantic import BaseModel
from typing import Optional
from fastapi import Form

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