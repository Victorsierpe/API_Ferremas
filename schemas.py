from pydantic import BaseModel, EmailStr # 
from typing import Optional 
from datetime import datetime 


class PrecioHistoricoBase(BaseModel): 
    fecha: Optional[datetime] = None
    precio: float


class PrecioHistoricoCreate(PrecioHistoricoBase):
    producto_id: int


class PrecioHistorico(PrecioHistoricoBase):
    id: int
    producto_id: int

    model_config = {
        "from_attributes": True
    }


class ProductoCreate(BaseModel):
    codigo: str
    marca: str
    nombre: str
    modelo: str
    stock: int


class Producto(ProductoCreate):
    id: int

    model_config = {
        "from_attributes": True
    }


class ContactoBase(BaseModel):
    nombre: str
    email: EmailStr
    mensaje: str


class ContactoCreate(ContactoBase):
    pass


class Contacto(ContactoBase):
    id: int

    model_config = {
        "from_attributes": True
    }
