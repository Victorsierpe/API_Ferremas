from transbank.webpay.webpay_plus.transaction import Transaction # Importar la clase Transaction de Webpay Plus
from fastapi import APIRouter # Importar APIRouter de FastAPI
from transbank.common.integration_type import IntegrationType 

# Configuración en modo TEST (sandbox oficial de Transbank)
Transaction.commerce_code = "597055555532"  # Código de comercio de prueba
Transaction.api_key = "597055555532"        # API key de prueba
Transaction.integration_type = IntegrationType.TEST  # Entorno de integración

RETURN_URL = "http://localhost:8000/pagos/confirmacion" # URL de retorno para la confirmación de la transacción

router = APIRouter() # Crear una instancia de APIRouter para definir las rutas

def iniciar_transaccion(buy_order: str, session_id: str, amount: int): # Función para iniciar una transacción
    transaction = Transaction() # Crear una instancia de Transaction
    response = transaction.create(
        buy_order=buy_order,
        session_id=session_id,
        amount=amount,
        return_url=RETURN_URL # URL de retorno para la confirmación de la transacción
    )
    return response.token, response.url 

def confirmar_transaccion(token_ws: str): # Función para confirmar una transacción
    transaction = Transaction() # Crear una instancia de Transaction
    result = transaction.commit(token_ws) # Confirmar la transacción utilizando el token
    return result  # Función para obtener el estado de la transacción
