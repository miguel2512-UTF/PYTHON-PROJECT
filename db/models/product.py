from pydantic import BaseModel
from typing import Optional
from fastapi import Request, File

class Product(BaseModel):
    id: Optional[str]
    name: str
    description: str
    price: int
    stock: int
    image: Optional[str]
    state: bool

    async def as_form(
        request: Request 
    ):
        form = await request.form()
        id = form.get("id")
        name = form.get("name")
        description = form.get("description")
        price = form.get("price")
        stock = form.get("stock")
        state = form.get("state")
        if len(state)==0 or state.lower()=="true":
            state=True
        else:
            state=False

        return Product(
            id=id,
            name=name,
            description=description,
            price=price,
            stock=stock,
            state=state
        )