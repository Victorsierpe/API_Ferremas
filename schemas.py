from pydantic import BaseModel, EmailStr
from typing import Optional 
from datetime import datetime # Importa las bibliotecas necesarias

class PrecioHistoricoBase(BaseModel): # Define la clase base para los precios históricos
    fecha: Optional[datetime] = None
    precio: float

class PrecioHistoricoCreate(PrecioHistoricoBase): # Define la clase para crear precios históricos
    producto_id: int

class PrecioHistorico(PrecioHistoricoBase): # Define la clase para los precios históricos
    id: int
    producto_id: int

    class Config:
        orm_mode = True

class ProductoCreate(BaseModel): # Define la clase base para los productos
    codigo: str
    marca: str
    nombre: str
    modelo: str
    stock: int

class Producto(ProductoCreate): # Define la clase para los productos
    id: int
    class Config:
        orm_mode = True

class ContactoBase(BaseModel): # Define la clase base para los contactos
    nombre: str
    email: EmailStr
    mensaje: str

class ContactoCreate(ContactoBase): # Define la clase para crear contactos
    pass

class Contacto(ContactoBase): # Define la clase para los contactos
    id: int
    class Config:
        orm_mode = True
