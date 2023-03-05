from fastapi.templating import Jinja2Templates

class Settings:
    TEMPLATES = Jinja2Templates(directory="templates")
    PRODUCT_IMAGES_DIRECTORY = "static/assets/product_images/"