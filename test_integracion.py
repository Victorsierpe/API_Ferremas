import pytest # con pytest se pueden crear pruebas automatizadas
from httpx import AsyncClient, ASGITransport # AsyncClient permite hacer peticiones HTTP de manera asíncrona
from main import app # Importa la aplicación FastAPI desde el archivo main.py

transport = ASGITransport(app=app) # Crea un transporte ASGI para la aplicación FastAPI

@pytest.mark.asyncio # Marca la función de prueba como asíncrona
async def test_integracion_crear_producto_y_precio(): # Define una prueba para crear un producto y asociar un precio
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        producto = { # Define un producto de prueba
            "codigo": "PINTEG001",
            "nombre": "Producto integración",
            "marca": "TestMarca",
            "modelo": "TestModelo",
            "stock": 15
        }
        r1 = await ac.post("/products/productos/", json=producto) # Envía una petición POST para crear el producto
        assert r1.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        producto_id = r1.json()["id"] # Obtiene el ID del producto creado

        precio = { # Define un precio para asociar al producto
            "precio": 9900.0
        }
        r2 = await ac.post(f"/products/productos/{producto_id}/precios", json=precio) # Envía una petición POST para asociar el precio al producto
        assert r2.status_code == 200
        assert r2.json()["precio"] == 9900.0 # Verifica que el precio se haya asociado correctamente al producto


@pytest.mark.asyncio
async def test_integracion_leer_precios_historicos_de_producto():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        producto = {
            "codigo": "PINTEG002",
            "nombre": "Martillo integración",
            "marca": "Test",
            "modelo": "MX123",
            "stock": 5
        }
        res = await ac.post("/products/productos/", json=producto)
        assert res.status_code == 200
        producto_id = res.json()["id"]

        await ac.post(f"/products/productos/{producto_id}/precios", json={"precio": 4500.0})
        r2 = await ac.get(f"/products/productos/{producto_id}/precios")
        assert r2.status_code == 200
        assert isinstance(r2.json(), list)
        assert len(r2.json()) >= 1


@pytest.mark.asyncio
async def test_integracion_contacto_guardado_correctamente():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        contacto = {
            "nombre": "Integrador",
            "email": "integrador@test.com",
            "mensaje": "Esto es una prueba de integración"
        }
        r = await ac.post("/contact/", json=contacto)
        assert r.status_code == 200
        assert "Formulario recibido" in r.json()["mensaje"]


@pytest.mark.asyncio
async def test_integracion_producto_actualizado_con_efecto():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        producto = {
            "codigo": "PINTEG003",
            "nombre": "Producto a actualizar",
            "marca": "TestMarca",
            "modelo": "ViejoModelo",
            "stock": 10
        }
        await ac.post("/products/productos/", json=producto)
        actualizado = {
            "codigo": "PINTEG003",
            "nombre": "Producto actualizado",
            "marca": "TestMarca",
            "modelo": "NuevoModelo",
            "stock": 20
        }
        r = await ac.put("/products/productos/PINTEG003", json=actualizado)
        assert r.status_code == 200
        assert r.json()["modelo"] == "NuevoModelo"


@pytest.mark.asyncio
async def test_integracion_producto_eliminado_y_confirmado():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        producto = {
            "codigo": "PINTEG004",
            "nombre": "Producto eliminar",
            "marca": "Test",
            "modelo": "DEL01",
            "stock": 3
        }
        await ac.post("/products/productos/", json=producto)
        r = await ac.delete("/products/productos/PINTEG004")
        assert r.status_code == 200
        r2 = await ac.get("/products/productos/PINTEG004")
        assert r2.status_code == 404


@pytest.mark.asyncio
async def test_integracion_conversion_moneda_valida():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/currency/conversion/dolar-peso?monto=2")
        assert r.status_code == 200
        data = r.json()
        assert data["origen"] == "USD"
        assert data["destino"] == "CLP"
        assert data["monto_origen"] == 2


@pytest.mark.asyncio
async def test_integracion_pago_webpay_mock():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post("/webpay/iniciar", params={
            "buy_order": "ORDER123",
            "session_id": "SESSION123",
            "amount": 5000
        })
        assert r.status_code == 200
        assert "token" in r.json()
        assert "url" in r.json()


@pytest.mark.asyncio
async def test_integracion_listar_todos_los_productos():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/products/productos/")
        assert r.status_code == 200
        assert isinstance(r.json(), list)


@pytest.mark.asyncio
async def test_integracion_producto_no_repetido():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        producto = {
            "codigo": "PINTEG005",
            "nombre": "Producto único",
            "marca": "MarcaX",
            "modelo": "X123",
            "stock": 1
        }
        r1 = await ac.post("/products/productos/", json=producto)
        r2 = await ac.post("/products/productos/", json=producto)
        assert r1.status_code == 200
        assert r2.status_code == 400


@pytest.mark.asyncio
async def test_integracion_precio_no_asociado_a_producto_inexistente():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # ID inválido (9999 no existe)
        precio = {"precio": 10000.0}
        r = await ac.post("/products/productos/9999/precios", json=precio)
        assert r.status_code in [404, 500]  # Puede depender de cómo manejes errores en `crud.agregar_precio_historico`
