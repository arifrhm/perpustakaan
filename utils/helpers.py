from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from jwt import PyJWTError as JWTError
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta
from typing import Dict, Optional, List

import jwt

from config.db import SessionLocal
from models.all_models import User, Peminjaman
from schemas.all_schemas import Buku, PeminjamanBukuData, UserRole, CustomResponse

# Inisialisasi JWT
SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Inisialisasi security dan enkripsi password
security = HTTPBearer()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def create_custom_response(status_code: int, message: str, datas: List) -> CustomResponse:
    return CustomResponse(status_code=status_code, message=message, datas=datas)

# Fungsi bantuan untuk memeriksa apakah email memiliki domain yang benar
def is_valid_email(email: str) -> bool:
    valid_domains = ['gmail.com', 'hotmail.com']  # Tambahkan domain lain sesuai kebutuhan
    domain = email.split('@')[-1]
    return domain in valid_domains

# Fungsi bantuan untuk memeriksa kekuatan password
def is_strong_password(password: str) -> bool:
    return len(password) >= 8 and any(char.isupper() for char in password) and password.isalnum()

# Fungsi bantuan untuk menghasilkan hash dari password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Fungsi bantuan untuk memeriksa kecocokan password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Fungsi bantuan untuk membuat token JWT
def create_access_token(data: Dict[str, str], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Fungsi bantuan untuk mendekode token JWT
def decode_access_token(token: str) -> Dict[str, str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')

# Fungsi untuk melakukan registrasi user baru
def register_user(db: SessionLocal, email: str, password: str) -> int:
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail='Email already registered')
    if not is_valid_email(email):
        raise HTTPException(status_code=400, detail='Invalid email domain')
    if not is_strong_password(password):
        raise HTTPException(status_code=400, detail='Weak password')
    
    hashed_password = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password, role=UserRole.user)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User with id =  user.id created successfully"}


# Fungsi untuk melakukan login
def login(db: SessionLocal, email: str, password: str) -> Dict[str, str]:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid email or password')
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({'sub': str(user.id), 'role': user.role}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}

# Fungsi untuk memeriksa apakah user memiliki akses admin
def is_admin(role: str) -> bool:
    return role == UserRole.admin

# Fungsi untuk mencatat peminjaman buku oleh user
def catat_peminjaman_buku(db: SessionLocal, user_id: int, buku_id: int) -> PeminjamanBukuData:
    existing_peminjaman = db.query(Peminjaman).filter(Peminjaman.user_id == user_id).first()
    if existing_peminjaman:
        raise HTTPException(status_code=400, detail='You already borrowed a book')
    
    buku = db.query(Buku).filter(Buku.id == buku_id).first()
    if not buku:
        raise HTTPException(status_code=404, detail='Book not found')
    
    tanggal_peminjaman = datetime.utcnow()
    tanggal_pengembalian = None
    
    peminjaman = Peminjaman(user_id=user_id, buku_id=buku_id, tanggal_peminjaman=tanggal_peminjaman, tanggal_pengembalian=tanggal_pengembalian)
    db.add(peminjaman)
    db.commit()
    db.refresh(peminjaman)
    
    peminjaman_data = PeminjamanBukuData(buku=buku, tanggal_peminjaman=tanggal_peminjaman, tanggal_pengembalian=tanggal_pengembalian)
    return peminjaman_data

# Fungsi untuk mengembalikan buku yang dipinjam oleh user
def kembalikan_buku(db: SessionLocal, user_id: int) -> PeminjamanBukuData:
    peminjaman = db.query(Peminjaman).filter(Peminjaman.user_id == user_id).first()
    if not peminjaman:
        raise HTTPException(status_code=404, detail='No borrowed book found')
    
    buku = db.query(Buku).filter(Buku.id == peminjaman.buku_id).first()
    if not buku:
        raise HTTPException(status_code=500, detail='Internal server error')
    
    if peminjaman.tanggal_pengembalian:
        raise HTTPException(status_code=400, detail='Book already returned')
    
    peminjaman.tanggal_pengembalian = datetime.utcnow()
    db.commit()
    
    peminjaman_data = PeminjamanBukuData(buku=buku, tanggal_peminjaman=peminjaman.tanggal_peminjaman, tanggal_pengembalian=peminjaman.tanggal_pengembalian)
    return peminjaman_data