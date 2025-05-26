from fastapi import APIRouter, Depends # Importa las dependencias necesarias de FastAPI
from sqlalchemy.orm import Session  # Importa la clase Session de SQLAlchemy
from schemas import ContactoCreate  # Importa los esquemas de la aplicación
import crud # Importa los módulos de CRUD y esquemas
from database import get_db # Importa la función get_db para obtener la sesión de la base de datos

router = APIRouter() # Crea una instancia del router de FastAPI

@router.post("/contact/") # Define la ruta para crear un nuevo contacto
def enviar_contacto(contacto: ContactoCreate, db: Session = Depends(get_db)): # Define la función para crear un nuevo contacto
    nuevo_contacto = crud.crear_contacto(db, contacto) # Crea el nuevo contacto en la base de datos
    return {"mensaje": "Formulario recibido", "contacto": nuevo_contacto} # Devuelve un mensaje de éxito y el contacto creado
