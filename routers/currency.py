from fastapi import APIRouter, HTTPException, Query
import bcchapi # Librería para acceder al Banco Central de Chile
import numpy as np

router = APIRouter()

siete = bcchapi.Siete(file="credentials.txt") # Inicializa la conexión con el Banco Central usando credenciales

@router.get("/conversion/dolar-peso")
async def conversion_dolar_peso(monto: float = Query(1.0, gt=0, description="Monto en USD a convertir")):
    try:
        serie_dolar = "F073.TCO.PRE.Z.D" # Código de la serie del dólar observado

        df = siete.cuadro(
            series=[serie_dolar],# CRealice una petición al BCCh para recuperar la última tasa de cambio USD/CLP.
            nombres=["dolar"], # Nombre de la serie
            desde=None,   # Fecha de inicio (None para obtener todos los datos)
            hasta=None, # Fecha de fin (None para obtener todos los datos)
            frecuencia="D",  # Diario
            observado={"dolar": "last"}  # Valor más reciente reportado
        )

        if df.empty or "dolar" not in df.columns:
            raise HTTPException(status_code=500, detail="No fue posible obtener el tipo de cambio del dólar.")

        valor_dolar = df["dolar"].iloc[-1]  # Último valor registrado

        valor_convertido = monto * valor_dolar # Conversión a CLP

        return {
            "origen": "USD",
            "destino": "CLP",
            "monto_origen": monto,
            "valor_unitario": valor_dolar,
            "valor_convertido": valor_convertido
        } 

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar tasa de cambio: {str(e)}")