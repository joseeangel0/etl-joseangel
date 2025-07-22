# TODO: Funciones de conexión y escritura/lectura en MongoDB
from pymongo import MongoClient

def get_mongo_db():
    client = MongoClient("host.docker.internal", 27018)
    return client["project2"]
