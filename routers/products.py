from fastapi import APIRouter, Depends, HTTPException # Importar dependencias de FastAPI
from sqlalchemy.orm import Session # Importar Session de SQLAlchemy
import crud, schemas # Importar funciones CRUD y esquemas de Pydantic
from database import get_db # Importar función para obtener la sesión de la base de datos

router = APIRouter() # Crear un router de FastAPI para manejar las rutas relacionadas con productos

@router.post("/productos/", response_model=schemas.Producto) # Definir endpoint para crear un producto
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)): # Este endpoint recibe un producto y lo crea en la base de datos
    db_producto = crud.get_producto_by_codigo(db, producto.codigo) # Verificar si el producto ya existe por su código
    if db_producto:
        raise HTTPException(status_code=400, detail="El código del producto ya existe.") # Si el producto ya existe, lanzar una excepción HTTP 400
    return crud.create_producto(db, producto) # Crear el producto en la base de datos usando la función CRUD

@router.get("/productos/{codigo}", response_model=schemas.Producto) # Definir endpoint para leer un producto por su código
def leer_producto(codigo: str, db: Session = Depends(get_db)): # Definir endpoint para leer un producto por su código
    db_producto = crud.get_producto_by_codigo(db, codigo) # Leer un producto existente en la base de datos por su código
    if db_producto is None: # Verificar si el producto existe por su código
        raise HTTPException(status_code=404, detail="Producto no encontrado") # Verificar si el producto existe por su código
    return db_producto # Leer un producto existente en la base de datos por su código, si no se encuentra, lanzar una excepción HTTP 404

@router.get("/productos/", response_model=list[schemas.Producto]) # Definir endpoint para listar productos
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)): # Definir endpoint para listar productos con paginación
    return crud.get_productos(db, skip=skip, limit=limit) # Listar productos con paginación, permite saltar un número de productos y limitar la cantidad de productos devueltos

@router.put("/productos/{codigo}", response_model=schemas.Producto) # Definir endpoint para actualizar un producto por su código
def actualizar_producto(codigo: str, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = crud.update_producto(db, codigo, producto) # Actualizar un producto existente en la base de datos por su código
    if db_producto is None: # Verificar si el producto existe por su código
        raise HTTPException(status_code=404, detail="Producto no encontrado") # Verificar si el producto existe por su código
    return db_producto # Actualizar un producto existente en la base de datos por su código

@router.delete("/productos/{codigo}") # Definir endpoint para eliminar un producto por su código
def eliminar_producto(codigo: str, db: Session = Depends(get_db)): # Definir endpoint para eliminar un producto por su código
    success = crud.delete_producto(db, codigo) # Eliminar un producto de la base de datos por su código
    if not success: # Verificar si el producto fue eliminado correctamente
        raise HTTPException(status_code=404, detail="Producto no encontrado") # Si no se encuentra el producto, lanzar una excepción HTTP 404
    return {"mensaje": "Producto eliminado correctamente"} # Eliminar un producto de la base de datos por su código

@router.post("/productos/{producto_id}/precios", response_model=schemas.PrecioHistorico) # Definir endpoint para crear un precio histórico para un producto
def crear_precio_historico(producto_id: int, precio: schemas.PrecioHistoricoBase, db: Session = Depends(get_db)): # Este endpoint recibe un ID de producto y un precio, y crea un nuevo precio histórico para ese producto
    # Validar que el producto exista
    db_producto = crud.get_producto_by_id(db, producto_id) # Obtener el producto por su ID
    if not db_producto: # Verificar si el producto existe por su ID
        raise HTTPException(status_code=404, detail="Producto no encontrado") # Si el producto no existe, lanzar una excepción HTTP 404

    return crud.agregar_precio_historico(# Crear un nuevo precio histórico para un producto
        db,
        schemas.PrecioHistoricoCreate(producto_id=producto_id, **precio.model_dump()) # Usar model_dump() para convertir el esquema a un diccionario
    )

@router.get("/productos/{producto_id}/precios", response_model=list[schemas.PrecioHistorico]) # Definir endpoint para leer precios históricos de un producto
def leer_precios_historicos(producto_id: int, db: Session = Depends(get_db)): # Verificar si el producto existe
    return crud.obtener_precios_historicos(db, producto_id) # Obtener los precios históricos del producto por su ID
