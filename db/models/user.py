from pydantic import BaseModel
from typing import Optional

# Entidad Usuario
class Usuario(BaseModel):
    id: Optional[str]
    username: str
    email: str