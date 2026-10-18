# Carga los datos de todas las capas en las bases de Chroma.
# Uso (desde cualquier carpeta):  python ChatBot-API/cargar_datos.py
# Se puede ejecutar las veces que quieras: los datos se reemplazan, no se duplican.
import os
import sys

# Las rutas del proyecto ("./app/...", "./chroma_db") son relativas a ChatBot-API/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)

from app.services.sChatbot2 import ChatbotService2

service = ChatbotService2()

errores = 0
for layer in service.DATA_FILES:
    try:
        print(f"{layer}: {service.uploadDatabase(layer)}")
    except Exception as e:
        errores += 1
        print(f"{layer}: ERROR -> {e}")

sys.exit(1 if errores else 0)
