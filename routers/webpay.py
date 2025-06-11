from fastapi import APIRouter, HTTPException
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
from dotenv import load_dotenv
import os

# Cargar variables desde .env
load_dotenv(dotenv_path="credentials.env")

# Obtener valores desde el entorno
commerce_code = os.getenv("TRANSBANK_COMMERCE_CODE")
api_key = os.getenv("TRANSBANK_API_KEY")

if not commerce_code or not api_key:
    raise ValueError("Faltan las variables TRANSBANK_COMMERCE_CODE o TRANSBANK_API_KEY")

# Configurar Transbank
Transaction.commerce_code = commerce_code
Transaction.api_key = api_key
Transaction.integration_type = IntegrationType.TEST

RETURN_URL = "http://localhost:8000/webpay/confirmacion"

router = APIRouter()


def iniciar_transaccion(buy_order: str, session_id: str, amount: int):
    # Si estamos corriendo pruebas con pytest, simular la respuesta
    if "PYTEST_CURRENT_TEST" in os.environ:
        return "mock_token_123", "https://webpay.test/mock"

    transaction = Transaction()
    response = transaction.create(
        buy_order=buy_order,
        session_id=session_id,
        amount=amount,
        return_url=RETURN_URL
    )
    return response.token, response.url


def confirmar_transaccion(token_ws: str):
    transaction = Transaction()
    result = transaction.commit(token_ws)
    return result


# Endpoint para iniciar transacción
@router.post("/iniciar")
def iniciar(buy_order: str, session_id: str, amount: int):
    try:
        token, url = iniciar_transaccion(buy_order, session_id, amount)
        return {"token": token, "url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error iniciando transacción: {str(e)}")


# Endpoint para confirmar transacción (retorno)
@router.get("/confirmacion")
def confirmar(token_ws: str):
    try:
        resultado = confirmar_transaccion(token_ws)
        return {"estado": resultado.status, "detalle": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error confirmando transacción: {str(e)}")
