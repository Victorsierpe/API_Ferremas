import pytest # Importa pytest para las pruebas
from httpx import AsyncClient, ASGITransport # Importa AsyncClient y ASGITransport para hacer peticiones HTTP asíncronas
from main import app # Importa la aplicación FastAPI desde el archivo main.py

transport = ASGITransport(app=app) # Crea un transporte ASGI para la aplicación FastAPI



@pytest.mark.asyncio # Marca la función de prueba como asíncrona
async def test_automatizado_ciclo_producto_completo(): # Test para realizar un ciclo completo de creación, obtención, actualización y eliminación de un producto
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        # Paso 1: Eliminar si ya existe
        await ac.delete("/products/productos/PAUTO001")

        # Paso 2: Crear producto
        producto = {
            "codigo": "PAUTO001",
            "nombre": "Producto auto test",
            "marca": "AutoMarca",
            "modelo": "AutoModelo",
            "stock": 100
        } # Define un producto de prueba
        r1 = await ac.post("/products/productos/", json=producto) # Envía una petición POST para crear el producto
        assert r1.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert r1.json()["codigo"] == "PAUTO001" # Verifica que el código del producto creado sea el esperado

        # Paso 3: Obtener producto
        r2 = await ac.get("/products/productos/PAUTO001") # Envía una petición GET para obtener el producto por su código
        assert r2.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert r2.json()["modelo"] == "AutoModelo" # Verifica que el modelo del producto obtenido sea el esperado

        # Paso 4: Actualizar producto
        actualizado = {
            "codigo": "PAUTO001",
            "nombre": "Producto actualizado",
            "marca": "AutoMarca",
            "modelo": "NuevoModelo",
            "stock": 150
        }
        r3 = await ac.put("/products/productos/PAUTO001", json=actualizado) # Envía una petición PUT para actualizar el producto
        assert r3.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert r3.json()["modelo"] == "NuevoModelo" # Verifica que el modelo del producto actualizado sea el esperado

        # Paso 5: Eliminar producto
        r4 = await ac.delete("/products/productos/PAUTO001") # Envía una petición DELETE para eliminar el producto
        assert r4.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)

        # Paso 6: Verificar que ya no existe
        r5 = await ac.get("/products/productos/PAUTO001") # Envía una petición GET para verificar que el producto ya no existe
        assert r5.status_code == 404 # Verifica que la respuesta sea un error 404 (producto no encontrado)


# Validar conversión de moneda y simulación de pago Webpay

@pytest.mark.asyncio # Marca la función de prueba como asíncrona
async def test_automatizado_conversion_y_webpay(): # Test para validar la conversión de moneda y simulación de pago Webpay
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        # Paso 1: Convertir moneda
        r1 = await ac.get("/currency/conversion/dolar-peso?monto=10") # Envía una petición GET para convertir 10 USD a CLP
        assert r1.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        data = r1.json() # Obtiene los datos de la respuesta
        assert data["origen"] == "USD" # Verifica que la moneda de origen sea USD
        assert data["destino"] == "CLP" # Verifica que la moneda de destino sea CLP
        assert data["monto_origen"] == 10 # Verifica que el monto de origen sea 10

        # Paso 2: Simular pago Webpay (mock si estás en pytest)
        r2 = await ac.post("/webpay/iniciar", params={ 
            "buy_order": "AUTOORDER123", # Orden de compra simulada
            "session_id": "AUTOSESSION456", # ID de sesión simulado
            "amount": 7500 # Monto simulado en CLP
        }) # Envía una petición POST para iniciar el pago Webpay
        assert r2.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert "token" in r2.json() # Verifica que el token de pago esté presente en la respuesta
        assert "url" in r2.json() # Verifica que la URL de pago esté presente en la respuesta

