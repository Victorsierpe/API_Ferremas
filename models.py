from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey # Importa las clases necesarias de SQLAlchemy
from database import Base # Importa la clase Base de la base de datos
from sqlalchemy.orm import relationship # Importa la relación de SQLAlchemy
from datetime import datetime # Importa la clase datetime de la biblioteca datetime

# Define los modelos de la base de datos
class Producto(Base):# Define la clase Producto que hereda de Base
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True) # Define el ID del producto como clave primaria y con índice
    codigo = Column(String, unique=True, index=True) # Define el código del producto como una cadena única y con índice
    nombre = Column(String) # Define el nombre del producto como una cadena
    marca = Column(String) # Define la marca del producto como una cadena
    modelo = Column(String) # Define el modelo del producto como una cadena
    stock = Column(Integer) # Define el stock del producto como un entero

    precios_historicos = relationship("PrecioHistorico", back_populates="producto")# Relación con la clase PrecioHistorico

class PrecioHistorico(Base):# Define la clase PrecioHistorico que hereda de Base
    __tablename__ = "precios_historicos" # Define la tabla precios_historicos
    id = Column(Integer, primary_key=True, index=True) # Define el ID del precio histórico como clave primaria y con índice
    producto_id = Column(Integer, ForeignKey("productos.id")) # Define el ID del producto como clave foránea que referencia a la tabla productos
    fecha = Column(DateTime, default=datetime.utcnow) # Define la fecha del precio histórico como una fecha y hora, con valor por defecto de la fecha y hora actual
    precio = Column(Float) # Define el precio del producto como un número de punto flotante

    producto = relationship("Producto", back_populates="precios_historicos")# Relación con la clase Producto

class Contacto(Base):# Define la clase Contacto que hereda de Base
    __tablename__ = "contactos" # Define la tabla contactos
    id = Column(Integer, primary_key=True, index=True) # Define el ID del contacto como clave primaria y con índice
    nombre = Column(String) # Define el nombre del contacto como una cadena
    email = Column(String) # Define el email del contacto como una cadena
    mensaje = Column(String) # Define el mensaje del contacto como una cadena

class Pago(Base):# Define la clase Pago que hereda de Base
    __tablename__ = "pagos" # Define la tabla pagos
    id = Column(Integer, primary_key=True, index=True) # Define el ID del pago como clave primaria y con índice
    codigo_producto = Column(String) # Define el código del producto asociado al pago como una cadena
    monto_pagado = Column(Float) # Define el monto pagado como un número de punto flotante
    estado = Column(String) # Define el estado del pago como una cadena 