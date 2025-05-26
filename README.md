# API_Ferremas
Dependencias instaladas vía pip

fastapi: Framework principal para la construcción de la API REST. (pip install fastapi)

uvicorn: Servidor ASGI para correr la aplicación FastAPI. (pip install uvicorn)

sqlalchemy: ORM para interactuar con la base de datos SQLite. (pip install sqlalchemy)

pydantic: Validación y serialización de datos. (pip install pydantic)

python-multipart: Soporte para formularios (por ejemplo, pagos Webpay). (pip install python-multipart)

requests: Consumir APIs externas “Banco Central”. (pip install requests) y (pip install bcchapi)

transbank-sdk: SDK oficial de Transbank para integrar Webpay Plus. ( pip install transbank-sdk )

Para ejecutar el servidor ingresamos este comando:  uvicorn main:app --reload

Para Probar la API: 
Usando la documentación automática de Swagger en: http://localhost:8000/docs o mediante una colección Postman proporcionada para pruebas funcionales de cada endpoint.

