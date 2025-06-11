from pydantic import BaseModel, EmailStr # importa BaseModel y EmailStr de pydantic
from typing import Optional  # importa Optional de typing
from datetime import datetime # importa datetime de datetime


class PrecioHistoricoBase(BaseModel): # Define la clase base para los precios históricos
    fecha: Optional[datetime] = None # Define la fecha como un campo opcional, con valor por defecto None
    precio: float # Define el precio como un campo obligatorio de tipo float


class PrecioHistoricoCreate(PrecioHistoricoBase):# Define la clase para crear un precio histórico, hereda de PrecioHistoricoBase
    producto_id: int # Define el ID del producto como un campo obligatorio de tipo int


class PrecioHistorico(PrecioHistoricoBase): # Define la clase para un precio histórico, hereda de PrecioHistoricoBase
    id: int # Define el ID del precio histórico como un campo obligatorio de tipo int
    producto_id: int # Define el ID del producto asociado al precio histórico como un campo obligatorio de tipo int

    model_config = { # Configuración del modelo para permitir la creación de instancias a partir de atributos
        "from_attributes": True # Permite crear instancias del modelo a partir de atributos
    }


class ProductoCreate(BaseModel): # Define la clase base para crear un producto
    codigo: str # Define el código del producto como un campo obligatorio de tipo str
    marca: str # Define la marca del producto como un campo obligatorio de tipo str
    nombre: str # Define el nombre del producto como un campo obligatorio de tipo str
    modelo: str # Define el modelo del producto como un campo obligatorio de tipo str
    stock: int # Define el stock del producto como un campo obligatorio de tipo int


class Producto(ProductoCreate): # Define la clase para un producto, hereda de ProductoCreate
    id: int # Define el ID del producto como un campo obligatorio de tipo int

    model_config = { # Configuración del modelo para permitir la creación de instancias a partir de atributos
        "from_attributes": True # Permite crear instancias del modelo a partir de atributos
    }


class ContactoBase(BaseModel): # Define la clase base para un contacto
    nombre: str # Define el nombre del contacto como un campo obligatorio de tipo str
    email: EmailStr # Define el email del contacto como un campo obligatorio de tipo EmailStr
    mensaje: str # Define el mensaje del contacto como un campo obligatorio de tipo str


class ContactoCreate(ContactoBase): # Define la clase para crear un contacto, hereda de ContactoBase
    pass # No se añaden campos adicionales, solo hereda de ContactoBase


class Contacto(ContactoBase): # Define la clase para un contacto, hereda de ContactoBase
    id: int # Define el ID del contacto como un campo obligatorio de tipo int

    model_config = { # Configuración del modelo para permitir la creación de instancias a partir de atributos
        "from_attributes": True # Permite crear instancias del modelo a partir de atributos
    }
