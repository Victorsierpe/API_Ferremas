
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_crear_producto_exitoso():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        producto = {
            "codigo": "PTEST001",
            "nombre": "Martillo prueba",
            "marca": "Stanley",
            "modelo": "M123",
            "stock": 10
        }
        response = await ac.post("/products/productos/", json=producto)
        assert response.status_code == 200
        assert response.json()["codigo"] == "PTEST001"

@pytest.mark.asyncio
async def test_crear_producto_repetido():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        producto = {
            "codigo": "PTEST001",
            "nombre": "Duplicado",
            "marca": "Stanley",
            "modelo": "M123",
            "stock": 5
        }
        response = await ac.post("/products/productos/", json=producto)
        assert response.status_code == 400

@pytest.mark.asyncio
async def test_obtener_producto():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/products/productos/PTEST001")
        assert response.status_code == 200
        assert response.json()["codigo"] == "PTEST001"

@pytest.mark.asyncio
async def test_producto_no_encontrado():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/products/productos/INEXISTENTE")
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_listar_productos():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/products/productos/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_actualizar_producto():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        producto_actualizado = {
            "codigo": "PTEST001",
            "nombre": "Martillo actualizado",
            "marca": "Stanley",
            "modelo": "M999",
            "stock": 20
        }
        response = await ac.put("/products/productos/PTEST001", json=producto_actualizado)
        assert response.status_code == 200
        assert response.json()["modelo"] == "M999"

@pytest.mark.asyncio
async def test_eliminar_producto():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.delete("/products/productos/PTEST001")
        assert response.status_code == 200
        assert response.json()["mensaje"] == "Producto eliminado correctamente"

@pytest.mark.asyncio
async def test_eliminar_producto_inexistente():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.delete("/products/productos/NO_EXISTE")
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_enviar_contacto():# Test para enviar contacto exitoso
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        contacto = {
            "nombre": "Carlos Tester",
            "email": "test@example.com",
            "mensaje": "Esto es una prueba"
        }
        response = await ac.post("/contact/", json=contacto) # Enviar contacto
        assert response.status_code == 200
        assert "Formulario recibido" in response.json()["mensaje"] # Verifica que el mensaje de éxito esté presente en la respuesta

@pytest.mark.asyncio # Test para enviar contacto con email inválido
async def test_enviar_contacto_email_invalido(): 
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        contacto = {
            "nombre": "Carlos",
            "email": "email_invalido",
            "mensaje": "Mensaje de prueba"
        }
        response = await ac.post("/contact/", json=contacto)# Enviar contacto con email inválido
        assert response.status_code == 422 # Verifica que el email inválido retorne un error 422
