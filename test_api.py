import pytest # Importar pytest para pruebas asíncronas
from httpx import AsyncClient, ASGITransport # Importar AsyncClient y ASGITransport para hacer peticiones HTTP asíncronas
from main import app # Importar la aplicación FastAPI desde el archivo main.py

transport = ASGITransport(app=app) # Crear un transporte ASGI para la aplicación FastAPI
#1 Prueba de la API de productos
@pytest.mark.asyncio # Marca la función de prueba como asíncrona
async def test_crear_producto_exitoso(): # Test para crear un producto exitosamente
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        producto = { # Define un producto de prueba
            "codigo": "PTEST001",
            "nombre": "Martillo prueba",
            "marca": "Stanley",
            "modelo": "M123",
            "stock": 10
        }
        response = await ac.post("/products/productos/", json=producto) # Envía una petición POST para crear el producto
        assert response.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert response.json()["codigo"] == "PTEST001" # Verifica que el código del producto creado sea el esperado

#2 Test para crear un producto con código repetido
@pytest.mark.asyncio # Test para crear un producto con código repetido
async def test_crear_producto_repetido(): # Test para crear un producto con código repetido
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        producto = { # Define un producto de prueba con el mismo código que el anterior
            "codigo": "PTEST001",
            "nombre": "Duplicado",
            "marca": "Stanley",
            "modelo": "M123",
            "stock": 5
        }
        response = await ac.post("/products/productos/", json=producto) # Envía una petición POST para crear el producto
        assert response.status_code == 400 # Verifica que la respuesta sea un error 400 (código repetido)

#3 Test para obtener un producto por su código
@pytest.mark.asyncio # Test para obtener un producto por su código
async def test_obtener_producto(): # Test para obtener un producto por su código
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        response = await ac.get("/products/productos/PTEST001") # Envía una petición GET para obtener el producto por su código
        assert response.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert response.json()["codigo"] == "PTEST001" # Verifica que el código del producto obtenido sea el esperado

#4 Test para obtener un producto que no existe
@pytest.mark.asyncio # Test para obtener un producto que no existe
async def test_producto_no_encontrado(): # Test para obtener un producto que no existe
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        response = await ac.get("/products/productos/INEXISTENTE") # Envía una petición GET para obtener un producto que no existe
        assert response.status_code == 404 # Verifica que la respuesta sea un error 404 (producto no encontrado)

#5 Test para listar productos
@pytest.mark.asyncio # Test para listar productos
async def test_listar_productos(): # Test para listar productos
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        response = await ac.get("/products/productos/") # Envía una petición GET para listar productos
        assert response.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert isinstance(response.json(), list) # Verifica que la respuesta sea una lista

#6 Test para actualizar un producto
@pytest.mark.asyncio # Test para actualizar un producto
async def test_actualizar_producto(): # Test para actualizar un producto
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        producto_actualizado = { # Define un producto actualizado
            "codigo": "PTEST001",
            "nombre": "Martillo actualizado",
            "marca": "Stanley",
            "modelo": "M999",
            "stock": 20
        }
        response = await ac.put("/products/productos/PTEST001", json=producto_actualizado) # Envía una petición PUT para actualizar el producto
        assert response.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert response.json()["modelo"] == "M999" # Verifica que el modelo del producto actualizado sea el esperado

#7 Test para actualizar un producto que no existe
@pytest.mark.asyncio # Test para actualizar un producto que no existe
async def test_eliminar_producto(): # Test para eliminar un producto
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        response = await ac.delete("/products/productos/PTEST001") # Envía una petición DELETE para eliminar el producto
        assert response.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert response.json()["mensaje"] == "Producto eliminado correctamente" # Verifica que el mensaje de éxito esté presente en la respuesta

#8 Test para eliminar un producto que no existe
@pytest.mark.asyncio # Test para eliminar un producto que no existe
async def test_eliminar_producto_inexistente(): # Test para eliminar un producto que no existe
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        response = await ac.delete("/products/productos/NO_EXISTE") # Envía una petición DELETE para eliminar un producto que no existe
        assert response.status_code == 404 # Verifica que la respuesta sea un error 404 (producto no encontrado)

#9 Prueba de la API de precios históricos
@pytest.mark.asyncio # Test para crear un precio histórico exitosamente
async def test_enviar_contacto():# Test para enviar contacto exitoso 
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        contacto = { # Define un contacto de prueba
            "nombre": "Carlos Tester",
            "email": "test@example.com",
            "mensaje": "Esto es una prueba"
        }
        response = await ac.post("/contact/", json=contacto) # Enviar contacto
        assert response.status_code == 200 # Verifica que la respuesta sea exitosa (código 200)
        assert "Formulario recibido" in response.json()["mensaje"] # Verifica que el mensaje de éxito esté presente en la respuesta

#10 Test para enviar contacto con email inválido
@pytest.mark.asyncio # Test para enviar contacto con email inválido
async def test_enviar_contacto_email_invalido():  # Test para enviar contacto con email inválido
    async with AsyncClient(transport=transport, base_url="http://test") as ac: # Abre un cliente asíncrono para hacer peticiones HTTP
        contacto = { # Define un contacto de prueba con email inválido
            "nombre": "Carlos",
            "email": "email_invalido",
            "mensaje": "Mensaje de prueba"
        }
        response = await ac.post("/contact/", json=contacto)# Enviar contacto con email inválido
        assert response.status_code == 422 # Verifica que el email inválido retorne un error 422
