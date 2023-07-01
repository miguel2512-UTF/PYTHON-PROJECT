from fastapi import APIRouter, Request, File, UploadFile
from db.models.product import Product
from db.client import db_client
from db.schemas.product import product_schema, products_schema
from services.productService import ProductService
from bson import ObjectId
from fastapi.responses import HTMLResponse, RedirectResponse
from passlib.context import CryptContext
from config.settings import Settings
import shutil
import os

route = APIRouter(prefix="/product", tags=["product"])

templates = Settings.TEMPLATES

crypt = CryptContext(schemes=["bcrypt"])

@route.get("/")
async def product_home():
    return RedirectResponse("/product/list")

@route.get("/list", response_class=HTMLResponse)
async def products_list (request: Request):
    products = ProductService.findAll()
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
    product_dict = dict(product)
    product_dict["code"] = generate_product_code()

    new_product = ProductService.save(product_dict)
    id_product = new_product["id"]

    new_product["image"] = upload_product_image(id_product, file)
    ProductService.save(new_product)

    return RedirectResponse("/product", status_code=303)

def generate_product_code():
    products_len = len(ProductService.findAll())
    code_format = f"P00"
    product_code = code_format + str(products_len + 1)

    return product_code

def upload_product_image(id, file):
    try:
        imagename = ""
        if not len(file.filename) == 0:
            imagename=f"{id}{file.filename}"
            with open(Settings.PRODUCT_IMAGES_DIRECTORY+imagename, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
    
    return imagename

def delete_product_image(imagename):
    if imagename:
        os.remove(Settings.PRODUCT_IMAGES_DIRECTORY+imagename)

# Post - Actualizar
@route.post("/update")
async def update_product (request: Request, file: UploadFile = File(...)):
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
    id_product = ObjectId(product.id)
    code = ProductService.find_one("_id", id_product)["code"]
    oldimage = ProductService.find_one("_id", id_product)["image"]
    newimage = ""

    if(newimage != oldimage):
        if (not oldimage == ""):
            os.remove(Settings.PRODUCT_IMAGES_DIRECTORY+oldimage)

    product_dict["image"] = upload_product_image(id_product, file)
    product_dict["code"] = code

    ProductService.save(product_dict)
    
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

    return RedirectResponse("/product/list", status_code=303)

# Delete - Eliminar
@route.get("/delete/{id}", status_code=204)
async def delete_product (id: str):
    product = ProductService.delete(id)
    delete_product_image(product["image"])

    return RedirectResponse("/product/list", status_code=303)

# Remove Image
@route.get("/removeimage/{id}")
def remove_image_of_product (id: str):
    product = product_schema(db_client.product.find_one({"_id": ObjectId(id)}))
    if(not product["image"] == ""):
        os.remove(Settings.PRODUCT_IMAGES_DIRECTORY+product["image"])
    product["image"] = ""

    db_client.product.find_one_and_replace({"_id": ObjectId(id)}, product)

    return True

def buscar_product_por_columna (field: str, key):

    try:
        product = db_client.product.find_one({field:key})
        return Product(**product_schema(product))
    except:
        return {"error" : "No se ha encontrado el Product"}