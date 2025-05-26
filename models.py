from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import Base # Importa la clase Base de la base de datos
from sqlalchemy.orm import relationship # Importa la relación de SQLAlchemy
from datetime import datetime # Importa la clase datetime de la biblioteca datetime

# Define los modelos de la base de datos
class Producto(Base):# Define la clase Producto que hereda de Base
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    nombre = Column(String)
    marca = Column(String)
    modelo = Column(String)
    stock = Column(Integer)

    precios_historicos = relationship("PrecioHistorico", back_populates="producto")# Relación con la clase PrecioHistorico

class PrecioHistorico(Base):# Define la clase PrecioHistorico que hereda de Base
    __tablename__ = "precios_historicos"
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    fecha = Column(DateTime, default=datetime.utcnow)
    precio = Column(Float)

    producto = relationship("Producto", back_populates="precios_historicos")# Relación con la clase Producto

class Contacto(Base):# Define la clase Contacto que hereda de Base
    __tablename__ = "contactos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String)
    mensaje = Column(String)

class Pago(Base):# Define la clase Pago que hereda de Base
    __tablename__ = "pagos"
    id = Column(Integer, primary_key=True, index=True)
    codigo_producto = Column(String)
    monto_pagado = Column(Float)
    estado = Column(String)