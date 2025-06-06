from pydantic import BaseModel, EmailStr # importa BaseModel y EmailStr de pydantic
from typing import Optional #importa Optional para tipos que pueden ser None
from datetime import datetime # importa datetime para manejar fechas y horas

class PrecioHistoricoBase(BaseModel): # define la clase base para el historial de precios
    fecha: Optional[datetime] = None # define la fecha como opcional, con valor por defecto None
    precio: float # define el precio como un flotante

class PrecioHistoricoCreate(PrecioHistoricoBase): # define la clase para crear un historial de precios
    producto_id: int # define el ID del producto como un entero

class PrecioHistorico(PrecioHistoricoBase):
    id: int
    producto_id: int

    class Config:
        from_attributes = True

class ProductoCreate(BaseModel):
    codigo: str
    marca: str
    nombre: str
    modelo: str
    stock: int

class Producto(ProductoCreate):
    id: int

    class Config:
        from_attributes = True

class ContactoBase(BaseModel):
    nombre: str
    email: EmailStr
    mensaje: str

class ContactoCreate(ContactoBase):
    pass

class Contacto(ContactoBase):
    id: int

    class Config:
        from_attributes = True
