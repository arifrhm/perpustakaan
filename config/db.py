from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Konfigurasi database SQLAlchemy
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:12345678@127.0.0.1:5432/perpustakaan'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()