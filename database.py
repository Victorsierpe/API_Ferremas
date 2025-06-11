from sqlalchemy import create_engine # Importante para crear el motor de la base de datos
from sqlalchemy.orm import declarative_base # Importante para definir modelos
from sqlalchemy.orm import sessionmaker # Importante para manejar sesiones de la base de datos
# URL de conexión (en este caso, SQLite local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./Ferremas.db" # Cambia a tu base de datos preferida si es necesario

# Crea el engine y configura la sesión
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crea la sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal() # Crea una nueva sesión de base de datos
    try: # Intenta usar la sesión
        yield db # Devuelve la sesión para su uso
    finally: # Asegura que la sesión se cierre al finalizar
        db.close() # Cierra la sesión al finalizar