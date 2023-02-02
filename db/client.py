from pymongo import MongoClient

# Base de datos local
# db_client = MongoClient().dbfastapi

# Base de datos remota
db_client = MongoClient(host="mongodb+srv://admin:admin@cluster0.qeamd7c.mongodb.net/?retryWrites=true&w=majority").dbfastapi