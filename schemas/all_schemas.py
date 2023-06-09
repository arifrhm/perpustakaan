from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum

# Model untuk buku
class Buku(BaseModel):
    id: int
    judul: str
    pengarang: str
    tanggal_terbit: datetime

# Model untuk peminjaman buku
class PeminjamanBuku(BaseModel):
    buku_id: int

# Model untuk data peminjaman buku oleh user
class PeminjamanBukuData(BaseModel):
    buku: Buku
    tanggal_peminjaman: datetime
    tanggal_pengembalian: Optional[datetime]

# Model untuk data user
class UserInDB(BaseModel):
    id: int
    email: EmailStr
    role: str

# Model untuk login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Model untuk registrasi
class UserRegister(BaseModel):
    email: EmailStr
    password: str

# Enum untuk role user
class UserRole(str, Enum):
    admin = 'admin'
    user = 'user'

class CustomResponse(BaseModel):
    status_code: int
    message: str
    datas: List
