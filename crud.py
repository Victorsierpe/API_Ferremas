from sqlalchemy.orm import Session # Importa la clase Session de SQLAlchemy
import models, schemas # Importa los modelos y esquemas de la aplicación

def create_producto(db: Session, producto: schemas.ProductoCreate):  # Crea un nuevo producto en la base de datos
    db_producto = models.Producto(**producto.model_dump())  # Usar model_dump() en lugar de dict()
    db.add(db_producto) # Agrega el producto a la sesión de la base de datos
    db.commit() # Confirma los cambios en la base de datos
    db.refresh(db_producto)     # Refresca la instancia del producto para obtener el ID generado
    return db_producto # Devuelve el producto creado


def get_producto_by_codigo(db: Session, codigo: str): # Obtiene un producto por su código
    return db.query(models.Producto).filter(models.Producto.codigo == codigo).first() # Devuelve el primer producto que coincide con el código
def get_productos(db: Session, skip: int = 0, limit: int = 100): # Obtiene una lista de productos con paginación
    return db.query(models.Producto).offset(skip).limit(limit).all() # Devuelve una lista de productos con un límite y un desplazamiento especificados

def agregar_precio_historico(db: Session, precio: schemas.PrecioHistoricoCreate): # Agrega un nuevo precio histórico a la base de datos
    db_precio = models.PrecioHistorico(**precio.model_dump())  # Usar model_dump()
    db.add(db_precio) # Agrega el precio a la sesión de la base de datos
    db.commit() # Confirma los cambios en la base de datos
    db.refresh(db_precio) # Refresca la instancia del precio para obtener el ID generado
    return db_precio # Devuelve el precio histórico creado


def obtener_precios_historicos(db: Session, producto_id: int): # Obtiene los precios históricos de un producto por su ID
    return db.query(models.PrecioHistorico).filter(models.PrecioHistorico.producto_id == producto_id).all() # Devuelve una lista de precios históricos que coinciden con el ID del producto

def crear_contacto(db: Session, contacto: schemas.ContactoCreate): # Crea un nuevo contacto en la base de datos
    db_contacto = models.Contacto(**contacto.model_dump())  # Usar model_dump()
    db.add(db_contacto) # Agrega el contacto a la sesión de la base de datos
    db.commit() # Confirma los cambios en la base de datos
    db.refresh(db_contacto) # Refresca la instancia del contacto para obtener el ID generado
    return db_contacto # Devuelve el contacto creado


def update_producto(db: Session, codigo: str, producto: schemas.ProductoCreate): # Actualiza un producto existente en la base de datos por su código
    db_producto = get_producto_by_codigo(db, codigo) # Obtiene el producto por su código
    if db_producto is None: # Si no se encuentra el producto, devuelve None
        return None 
    for key, value in producto.model_dump().items():  # Usar model_dump() en lugar de dict()
        setattr(db_producto, key, value) # Actualiza los atributos del producto con los nuevos valores
    db.commit() # Confirma los cambios en la base de datos
    db.refresh(db_producto) # Refresca la instancia del producto para obtener los cambios actualizados
    return db_producto # Devuelve el producto actualizado


def delete_producto(db: Session, codigo: str): # Elimina un producto de la base de datos por su código
    db_producto = get_producto_by_codigo(db, codigo) # Obtiene el producto por su código
    if db_producto is None: # Si no se encuentra el producto, devuelve False
        return False
    db.delete(db_producto) # Elimina el producto de la sesión de la base de datos
    db.commit() # Confirma los cambios en la base de datos
    return True # Devuelve True si el producto fue eliminado con éxito

def get_producto_by_id(db: Session, producto_id: int): # Obtiene un producto por su ID
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first() # Devuelve el primer producto que coincide con el ID
