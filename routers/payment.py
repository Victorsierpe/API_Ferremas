from fastapi import APIRouter, Form # Importar APIRouter y Form de FastAPI
from routers.webpay import iniciar_transaccion, confirmar_transaccion # Importar las funciones de transacción
from fastapi.responses import HTMLResponse # Importar HTMLResponse de FastAPI

router = APIRouter(prefix="/pagos", tags=["Pagos"]) # Crear una instancia de APIRouter para definir las rutas

@router.post("/iniciar") # Ruta para iniciar una transacción
async def iniciar_pago(amount: int = Form(...), buy_order: str = Form(...), session_id: str = Form(...)):  # Parámetros de la transacción
    token, url = iniciar_transaccion(buy_order, session_id, amount) # Llamar a la función para iniciar la transacción
    return {"token": token, "url": url} # Devolver el token y la URL de la transacción iniciada

@router.get("/confirmacion", response_class=HTMLResponse) # Ruta para confirmar el pago
async def confirmar_pago(token_ws: str): # Parámetro token_ws para confirmar la transacción
    result = confirmar_transaccion(token_ws) # Llamar a la función para confirmar la transacción
    return f"<h1>Pago confirmado</h1><pre>{result}</pre>" # Devolver una respuesta HTML con el resultado de la transacción confirmada
