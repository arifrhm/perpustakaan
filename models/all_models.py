from config.db import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

# Model untuk tabel User
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)

# Model untuk tabel Peminjaman
class Peminjaman(Base):
    __tablename__ = 'peminjaman'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    buku_id = Column(Integer)
    tanggal_peminjaman = Column(DateTime, default=datetime.utcnow)
    tanggal_pengembalian = Column(DateTime)
