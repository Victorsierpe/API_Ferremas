from fastapi import APIRouter, HTTPException, Query
from dotenv import load_dotenv
import bcchapi
import os
import numpy as np

# Cargar variables desde el archivo .env
load_dotenv(dotenv_path="credentials.env")

# Obtener credenciales desde variables de entorno
email = os.getenv("BCCH_EMAIL")
password = os.getenv("BCCH_PASSWORD")

# Validación de credenciales
if not email or not password:
    raise ValueError("Faltan variables de entorno: BCCH_EMAIL o BCCH_PASSWORD")

# Inicializa la conexión con el Banco Central usando argumentos POSICIONALES
siete = bcchapi.Siete(email, password)

router = APIRouter()

@router.get("/conversion/dolar-peso")
async def conversion_dolar_peso(monto: float = Query(1.0, gt=0, description="Monto en USD a convertir")):
    try:
        serie_dolar = "F073.TCO.PRE.Z.D"

        df = siete.cuadro(
            series=[serie_dolar],
            nombres=["dolar"],
            desde=None,
            hasta=None,
            frecuencia="D",
            observado={"dolar": "last"}
        )

        if df.empty or "dolar" not in df.columns:
            raise HTTPException(status_code=500, detail="No fue posible obtener el tipo de cambio del dólar.")

        valor_dolar = df["dolar"].iloc[-1]
        valor_convertido = monto * valor_dolar

        return {
            "origen": "USD",
            "destino": "CLP",
            "monto_origen": monto,
            "valor_unitario": valor_dolar,
            "valor_convertido": valor_convertido
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar tasa de cambio: {str(e)}") 