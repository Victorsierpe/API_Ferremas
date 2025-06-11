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
def leer_producto(codigo: str, db: Session = Depends(get_db)):
    db_producto = crud.get_producto_by_codigo(db, codigo)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.get("/productos/", response_model=list[schemas.Producto])
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_productos(db, skip=skip, limit=limit)

@router.put("/productos/{codigo}", response_model=schemas.Producto)
def actualizar_producto(codigo: str, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = crud.update_producto(db, codigo, producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.delete("/productos/{codigo}")
def eliminar_producto(codigo: str, db: Session = Depends(get_db)):
    success = crud.delete_producto(db, codigo)
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado correctamente"}

@router.post("/productos/{producto_id}/precios", response_model=schemas.PrecioHistorico)
def crear_precio_historico(producto_id: int, precio: schemas.PrecioHistoricoBase, db: Session = Depends(get_db)):
    # Validar que el producto exista
    db_producto = crud.get_producto_by_id(db, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return crud.agregar_precio_historico(
        db,
        schemas.PrecioHistoricoCreate(producto_id=producto_id, **precio.model_dump())
    )

@router.get("/productos/{producto_id}/precios", response_model=list[schemas.PrecioHistorico])
def leer_precios_historicos(producto_id: int, db: Session = Depends(get_db)):
    return crud.obtener_precios_historicos(db, producto_id)
