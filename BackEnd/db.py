from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker,relationship
# load doenv
import os
from dotenv import load_dotenv


load_dotenv()
url_db = os.getenv("DATABASE_URL")
# cria banco local (arquivo)
DATABASE_URL = url_db

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # necessário pro SQLite
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()