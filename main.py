from fastapi import FastAPI # Importa FastAPI
from routers import products, contact, currency, webpay # Importa los routers de la aplicación
from database import engine # Importa el motor de la base de datos
import models # Importa los modelos de la aplicación

models.Base.metadata.create_all(bind=engine)    # Crea las tablas en la base de datos

app = FastAPI() # Crea una instancia de FastAPI

app.include_router(products.router, prefix="/products", tags=["Productos"])     # Incluye el router de productos
app.include_router(contact.router, tags=["Contacto"])   # Incluye el router de contacto
app.include_router(currency.router, prefix="/currency", tags=["Moneda"]) # Incluye el router de moneda
app.include_router(webpay.router, prefix="/webpay", tags=["Webpay"])    # Incluye el router de Webpay

@app.get("/") # Define la ruta raíz
async def root(): # Define la función para la ruta raíz
    return { "Tu API funciona correctamente"} # Devuelve un mensaje de éxito