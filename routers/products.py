from fastapi import APIRouter, Depends, HTTPException # Importa las dependencias necesarias de FastAPI
from sqlalchemy.orm import Session # Importa la clase Session de SQLAlchemy
import crud, schemas # Importa los módulos de CRUD y esquemas
from database import get_db # Importa la función get_db para obtener la sesión de la base de datos

router = APIRouter() # Crea una instancia del router de FastAPI

@router.post("/productos/", response_model=schemas.Producto) # Define la ruta para crear un nuevo producto
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)): # Define la función para crear un nuevo producto
    db_producto = crud.get_producto_by_codigo(db, producto.codigo) # Verifica si el producto ya existe
    if db_producto: # Si el producto ya existe, lanza una excepción HTTP
        raise HTTPException(status_code=400, detail="El código del producto ya existe.") 
    return crud.create_producto(db, producto) # Crea el nuevo producto en la base de datos

@router.get("/productos/{codigo}", response_model=schemas.Producto) # Define la ruta para obtener un producto por su código
def leer_producto(codigo: str, db: Session = Depends(get_db)): # Define la función para obtener un producto por su código
    db_producto = crud.get_producto_by_codigo(db, codigo) # Obtiene el producto por su código
    if db_producto is None: # Si el producto no existe, lanza una excepción HTTP
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto # Devuelve el producto encontrado

@router.get("/productos/", response_model=list[schemas.Producto]) # Define la ruta para obtener una lista de productos
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)): # Define la función para listar productos
    return crud.get_productos(db, skip=skip, limit=limit) # Devuelve una lista de productos con paginación

@router.put("/productos/{codigo}", response_model=schemas.Producto) # Define la ruta para actualizar un producto
def actualizar_producto(codigo: str, producto: schemas.ProductoCreate, db: Session = Depends(get_db)): # Define la función para actualizar un producto
    db_producto = crud.update_producto(db, codigo, producto) # Actualiza el producto en la base de datos
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado") # Si el producto no existe, lanza una excepción HTTP
    return db_producto # Devuelve el producto actualizado

@router.delete("/productos/{codigo}") # Define la ruta para eliminar un producto
def eliminar_producto(codigo: str, db: Session = Depends(get_db)): # Define la función para eliminar un producto
    success = crud.delete_producto(db, codigo) # Elimina el producto de la base de datos
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado") # Si el producto no existe, lanza una excepción HTTP
    return {"mensaje": "Producto eliminado correctamente"} # Devuelve un mensaje de éxito

@router.post("/productos/{producto_id}/precios", response_model=schemas.PrecioHistorico) # Define la ruta para crear un nuevo precio histórico
def crear_precio_historico(producto_id: int, precio: schemas.PrecioHistoricoBase, db: Session = Depends(get_db)): # Define la función para crear un nuevo precio histórico
    return crud.agregar_precio_historico(db, schemas.PrecioHistoricoCreate(producto_id=producto_id, **precio.dict())) # Crea el nuevo precio histórico en la base de datos

@router.get("/productos/{producto_id}/precios", response_model=list[schemas.PrecioHistorico]) # Define la ruta para obtener los precios históricos de un producto
def leer_precios_historicos(producto_id: int, db: Session = Depends(get_db)): # Define la función para obtener los precios históricos de un producto
    return crud.obtener_precios_historicos(db, producto_id) # Devuelve una lista de precios históricos del producto