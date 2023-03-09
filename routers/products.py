from fastapi import APIRouter, Request, File, UploadFile
from db.models.product import Product
from db.client import db_client
from db.schemas.product import product_schema, products_schema
from bson import ObjectId
from fastapi.responses import HTMLResponse, RedirectResponse
from passlib.context import CryptContext
from config.settings import Settings
import shutil

route = APIRouter(prefix="/product", tags=["product"])

templates = Settings.TEMPLATES

crypt = CryptContext(schemes=["bcrypt"])

@route.get("/")
async def product_home():
    return RedirectResponse("/product/list")

@route.get("/list", response_class=HTMLResponse)
async def products_list (request: Request):
    products = products_schema(list(db_client.product.find()))
    return templates.TemplateResponse("views/product/product.html",{"request": request, "products": products})

# Path
@route.get("/search/{code}")
async def product_by_id (code: str):
    return buscar_product_por_columna("code", code.upper())

# Get - Create Form
@route.get("/formcreate", response_class=HTMLResponse)
async def form_create(request: Request):
    return templates.TemplateResponse("views/product/create.html",{"request": request, "errors":"", "product":""})

# Get - Update Form
@route.get("/formupdate/{id}", response_class=HTMLResponse)
async def form_update(id: str, request: Request):
    product = product_schema(db_client.product.find_one({"_id": ObjectId(id)}))
    return templates.TemplateResponse("views/product/update.html",{"request":request, "errors":"", "product": product})

# Post - Crear
@route.post("/create/", status_code=201)
async def create_product (request: Request, file: UploadFile = File(...)):
    product: Product = await Product.as_form(request)
    # errors=Product.is_valid_product(product, action="create")

    """
    if errors:
        if type(buscar_product_por_columna(field="email", key=product.email)) == Product:
            errors["email"]="Email is already in use"
        return templates.TemplateResponse("views/product/create.html",{"request":request, "errors": errors, "product": product})

    if type(buscar_product_por_columna(field="email", key=product.email)) == Product:
        errors["email"]="Email is already in use"
        return templates.TemplateResponse("views/product/create.html",{"request":request, "errors": errors, "product": product})
    """ 

    product_dict = dict(product)
    # We generate the product code
    product_dict["code"] = f"P00{len(products_schema(list(db_client.product.find())))+1}"

    # We created the product and we take the id 
    id_product = db_client.product.insert_one(product_dict).inserted_id

    imagename=f"{id_product}{file.filename}"
    
    # Save us the image
    # Guardamos la imagen
    try:
        with open(Settings.PRODUCT_IMAGES_DIRECTORY+imagename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    # We consult the product and update the name of the image
    # Buscamos el producto y actualizamos el nombre de la imagen
    new_product = product_schema(db_client.product.find_one({"_id":id_product}))
    new_product["image"] = imagename
    del new_product["id"]
    # Save us the changes
    # Guardamos los cambios
    db_client.product.find_one_and_replace({"_id":ObjectId(id_product)}, new_product)

    return RedirectResponse("/product", status_code=303)

# Post - Actualizar
@route.post("/update")
async def update_product (request: Request):
    product: Product = await Product.as_form(request)
    # errors = Product.is_valid_product(product, action="update")
    # email_product = buscar_product_por_columna(field="email", key=product.email)

    # if errors:
    #     if type(email_product) == Product and product.id != email_product.id:
    #         errors["email"]="Email is already in use"
    #     return templates.TemplateResponse("views/product/update.html",{"request":request, "errors": errors, "product": product})

    # if type(email_product) == Product and product.id != email_product.id:
    #     errors["email"]="Email is already in use"
    #     return templates.TemplateResponse("views/product/update.html",{"request":request, "errors": errors, "product": product})

    product_dict = dict(product)
    image = product_schema(db_client.product.find_one({"_id": ObjectId(product.id)}))["image"]
    code = product_schema(db_client.product.find_one({"_id": ObjectId(product.id)}))["code"]
    product_dict["image"] = image
    product_dict["code"] = code
    del product_dict["id"]

    try:
        db_client.product.find_one_and_replace({"_id":ObjectId(product.id)}, product_dict)
    except:
        return {"error":"No se pudo actualizar el Product"}
    
    return RedirectResponse("/product", status_code=303)

# Active / Inactive
@route.get("/changestate/{id}", status_code=204)
async def toggle_state(id: str):
    product = product_schema(db_client.product.find_one({"_id":ObjectId(id)}))

    if product["state"] :
        product["state"] = False
        db_client.product.find_one_and_replace({"_id":ObjectId(id)}, product)
    else:
        product["state"] = True
        db_client.product.find_one_and_replace({"_id":ObjectId(id)}, product)

    return RedirectResponse("/product/list")

# Delete - Eliminar
@route.delete("/delete/{id}", status_code=204)
async def delete_product (id: str):

    found = db_client.product.find_one_and_delete({"_id":ObjectId(id)})

    if not found:
        return {"error":"El Product no pudo ser eliminado"}
    
    return {"message":"Product eliminado exitosamente"}

def buscar_product_por_columna (field: str, key):

    try:
        product = db_client.product.find_one({field:key})
        return Product(**product_schema(product))
    except:
        return {"error" : "No se ha encontrado el Product"}