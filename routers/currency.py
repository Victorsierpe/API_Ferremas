from fastapi import APIRouter, HTTPException, Query # Importar dependencias de FastAPI
from dotenv import load_dotenv # Importar para cargar variables de entorno
import bcchapi # Importar la API del Banco Central de Chile
import os # Importar para acceder a las variables de entorno

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

router = APIRouter() # Crear un router de FastAPI para manejar las rutas relacionadas con la conversión de divisas

@router.get("/conversion/dolar-peso")
async def conversion_dolar_peso(monto: float = Query(1.0, gt=0, description="Monto en USD a convertir")):
    """
    Convierte una cantidad en dólares (USD) a pesos chilenos (CLP) usando el valor más reciente del Banco Central.

    Args:
        monto (float): Monto en dólares a convertir. Debe ser mayor que 0.

    Returns:
        dict: Resultado de la conversión con tipo de cambio actual.
    """
    try:
        serie_dolar = "F073.TCO.PRE.Z.D"  # Código de la serie del dólar observado

        df = siete.cuadro(
            series=[serie_dolar],
            nombres=["dolar"],
            desde=None,
            hasta=None,
            frecuencia="D",
            observado={"dolar": "last"}
        )

        if df.empty or "dolar" not in df.columns: # Verifica si el DataFrame está vacío o no contiene la columna 'dolar'
            raise HTTPException(status_code=500, detail="No fue posible obtener el tipo de cambio del dólar.") # Si no se obtiene el tipo de cambio, lanza una excepción HTTP 500

        valor_dolar = df["dolar"].iloc[-1] # Obtiene el último valor del dólar observado
        valor_convertido = monto * valor_dolar # Calcula el valor convertido a pesos chilenos

        return {# Resultado de la conversión
            "origen": "USD",
            "destino": "CLP",
            "monto_origen": monto,
            "valor_unitario": valor_dolar,
            "valor_convertido": valor_convertido
        }

    except Exception as e: # Captura cualquier excepción que ocurra durante la consulta del tipo de cambio
        raise HTTPException(status_code=500, detail=f"Error al consultar tasa de cambio: {str(e)}") # Si ocurre un error, lanza una excepción HTTP 500 con el mensaje de error
