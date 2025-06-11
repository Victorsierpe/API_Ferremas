import pytest # Importa pytest para las pruebas
from httpx import AsyncClient, ASGITransport # Importa AsyncClient y ASGITransport para hacer peticiones HTTP asíncronas
from main import app # Importa la aplicación FastAPI desde el archivo main.py

transport = ASGITransport(app=app) # Crea un transporte ASGI para la aplicación FastAPI


@pytest.mark.asyncio # Marca la función de prueba como asíncrona
async def test_integracion_crear_producto_y_precio(): # Test para crear un producto y asociarle un precio
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        await ac.delete("/products/productos/PINTEG001") # Elimina el producto si ya existe

        producto = { # Define un producto de prueba
            "codigo": "PINTEG001", 
            "nombre": "Producto integración",
            "marca": "TestMarca",
            "modelo": "TestModelo",
            "stock": 15
        } # Crea un producto de prueba
        r1 = await ac.post("/products/productos/", json=producto) # Envía una petición POST para crear el producto
        assert r1.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        producto_id = r1.json()["id"] # Obtiene el ID del producto creado

        precio = {"precio": 9900.0} # Define un precio para el producto
        r2 = await ac.post(f"/products/productos/{producto_id}/precios", json=precio) # Envía una petición POST para asociar el precio al producto
        assert r2.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert r2.json()["precio"] == 9900.0 # Verifica que el precio asociado sea el esperado


@pytest.mark.asyncio # Test para obtener un producto por su código
async def test_integracion_leer_precios_historicos_de_producto(): # Test para leer los precios históricos de un producto
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        await ac.delete("/products/productos/PINTEG002") # Elimina el producto si ya existe

        producto = { # Define un producto de prueba
            "codigo": "PINTEG002",
            "nombre": "Martillo integración",
            "marca": "Test",
            "modelo": "MX123",
            "stock": 5
        } # Crea un producto de prueba
        res = await ac.post("/products/productos/", json=producto) # Envía una petición POST para crear el producto
        assert res.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        producto_id = res.json()["id"] # Obtiene el ID del producto creado

        await ac.post(f"/products/productos/{producto_id}/precios", json={"precio": 4500.0}) # Asocia un precio al producto
        r2 = await ac.get(f"/products/productos/{producto_id}/precios") # Envía una petición GET para obtener los precios históricos del producto
        assert r2.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert isinstance(r2.json(), list) # Verifica que la respuesta sea una lista
        assert len(r2.json()) >= 1 # Verifica que haya al menos un precio histórico asociado al producto


@pytest.mark.asyncio # Test para guardar un contacto a través del formulario
async def test_integracion_contacto_guardado_correctamente(): # Test para guardar un contacto a través del formulario
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        contacto = { # Define un contacto de prueba
            "nombre": "Integrador", 
            "email": "integrador@test.com",
            "mensaje": "Esto es una prueba de integración"
        } # Crea un contacto de prueba
        r = await ac.post("/contact/", json=contacto) # Envía una petición POST para guardar el contacto
        assert r.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert "Formulario recibido" in r.json()["mensaje"] # Verifica que el mensaje de respuesta contenga "Formulario recibido"


@pytest.mark.asyncio # Test para actualizar un producto con efecto
async def test_integracion_producto_actualizado_con_efecto(): # Test para actualizar un producto con efecto
    async with AsyncClient(transport=transport, base_url="http://test") as ac:# Abre un cliente asíncrono para hacer peticiones HTTP
        await ac.delete("/products/productos/PINTEG003") # Elimina el producto si ya existe

        producto = { # Define un producto de prueba
            "codigo": "PINTEG003",
            "nombre": "Producto a actualizar",
            "marca": "TestMarca",
            "modelo": "ViejoModelo",
            "stock": 10
        } # Crea un producto de prueba
        await ac.post("/products/productos/", json=producto) # Envía una petición POST para crear el producto

        actualizado = { # Define un producto actualizado
            "codigo": "PINTEG003",
            "nombre": "Producto actualizado",
            "marca": "TestMarca",
            "modelo": "NuevoModelo",
            "stock": 20
        } # Crea un producto actualizado
        r = await ac.put("/products/productos/PINTEG003", json=actualizado) # Envía una petición PUT para actualizar el producto
        assert r.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert r.json()["modelo"] == "NuevoModelo" # Verifica que el modelo del producto actualizado sea el esperado


@pytest.mark.asyncio # Test para eliminar un producto y confirmar su eliminación
async def test_integracion_producto_eliminado_y_confirmado(): # Test para eliminar un producto y confirmar su eliminación
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        producto = { # Define un producto de prueba
            "codigo": "PINTEG004",
            "nombre": "Producto eliminar",
            "marca": "Test",
            "modelo": "DEL01",
            "stock": 3
        } # Crea un producto de prueba
        await ac.delete("/products/productos/PINTEG004") # Elimina el producto si ya existe
        await ac.post("/products/productos/", json=producto) # Envía una petición POST para crear el producto

        r = await ac.delete("/products/productos/PINTEG004") # Envía una petición DELETE para eliminar el producto
        assert r.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)

        r2 = await ac.get("/products/productos/PINTEG004") # Envía una petición GET para intentar obtener el producto eliminado
        assert r2.status_code == 404 # Verifica que al intentar obtener el producto eliminado, se reciba un error 404 (producto no encontrado)


@pytest.mark.asyncio # Test para la conversión de moneda válida
async def test_integracion_conversion_moneda_valida(): # Test para la conversión de moneda válida
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        r = await ac.get("/currency/conversion/dolar-peso?monto=2") # Envía una petición GET para convertir 2 dólares a pesos chilenos
        assert r.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        data = r.json() # Obtiene los datos de la respuesta
        assert data["origen"] == "USD" # Verifica que la moneda de origen sea USD
        assert data["destino"] == "CLP" # Verifica que la moneda de destino sea CLP
        assert data["monto_origen"] == 2 # Verifica que el monto de origen sea 2


@pytest.mark.asyncio # Test para la conversión de moneda inválida
async def test_integracion_pago_webpay_mock(): # Test para la integración de pago con Webpay (mock)
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        r = await ac.post("/webpay/iniciar", params={ # Inicia el proceso de pago con Webpay
            "buy_order": "ORDER123", # Orden de compra
            "session_id": "SESSION123", # ID de sesión
            "amount": 5000 # Monto a pagar
        }) # Envía una petición POST para iniciar el pago
        assert r.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert "token" in r.json() # Verifica que la respuesta contenga un token
        assert "url" in r.json() # Verifica que la respuesta contenga una URL


@pytest.mark.asyncio # Test para listar todos los productos
async def test_integracion_listar_todos_los_productos(): # Test para listar todos los productos
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        r = await ac.get("/products/productos/") # Envía una petición GET para listar todos los productos
        assert r.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert isinstance(r.json(), list) # Verifica que la respuesta sea una lista


@pytest.mark.asyncio # Test para verificar que un producto no se pueda crear con un código repetido
async def test_integracion_producto_no_repetido(): # Test para verificar que un producto no se pueda crear con un código repetido
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        await ac.delete("/products/productos/PINTEG005") # Elimina el producto si ya existe

        producto = { # Define un producto de prueba
            "codigo": "PINTEG005",
            "nombre": "Producto único",
            "marca": "MarcaX",
            "modelo": "X123",
            "stock": 1
        }
        r1 = await ac.post("/products/productos/", json=producto) # Envía una petición POST para crear el producto
        r2 = await ac.post("/products/productos/", json=producto) # Intenta enviar una segunda petición POST para crear el mismo producto
        assert r1.status_code == 200 # Verifica que la primera respuesta sea exitosa (código 200)
        assert r2.status_code == 400 # Verifica que la segunda respuesta sea un error 400 (código repetido)


@pytest.mark.asyncio # Test para verificar que no se pueda asociar un precio a un producto inexistente
async def test_integracion_precio_no_asociado_a_producto_inexistente(): # Test para verificar que no se pueda asociar un precio a un producto inexistente
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        precio = {"precio": 10000.0} # Define un precio para el producto
        r = await ac.post("/products/productos/9999/precios", json=precio) # Intenta enviar una petición POST para asociar el precio a un producto inexistente
        assert r.status_code == 404 # Verifica que la respuesta sea un error 404 (producto no encontrado)
