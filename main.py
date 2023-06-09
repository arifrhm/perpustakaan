from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

import uvicorn

from config.db import SessionLocal, Base, engine
from config.connection import get_db
from utils.helpers import register_user,login,is_admin,catat_peminjaman_buku,decode_access_token, kembalikan_buku
from schemas.all_schemas import UserLogin, UserRegister, PeminjamanBukuData, PeminjamanBuku
from models.all_models import Peminjaman

app = FastAPI()

# Inisialisasi JWT
SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Inisialisasi security dan enkripsi password
security = HTTPBearer()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Endpoint untuk registrasi user
@app.post('/register', response_model=int)
def register(user_data: UserRegister, db: SessionLocal = Depends(get_db)):
    return register_user(db, user_data.email, user_data.password)

# Endpoint untuk login
@app.post('/login', response_model=Dict[str, str])
def login_user(user_data: UserLogin, db: SessionLocal = Depends(get_db)):
    return login(db, user_data.email, user_data.password)

# Endpoint untuk mencatat peminjaman buku
@app.post('/peminjaman', response_model=PeminjamanBukuData)
def peminjaman_buku(peminjaman_data: PeminjamanBuku, credentials: HTTPAuthorizationCredentials = Depends(security), db: SessionLocal = Depends(get_db)):
    token_payload = decode_access_token(credentials.credentials)
    user_id = int(token_payload['sub'])
    if not is_admin(token_payload['role']) and db.query(Peminjaman).filter(Peminjaman.user_id == user_id).first():
        raise HTTPException(status_code=400, detail='You already borrowed a book')
    
    return catat_peminjaman_buku(db, user_id, peminjaman_data.buku_id)

# Endpoint untuk mengembalikan buku
@app.post('/pengembalian', response_model=PeminjamanBukuData)
def pengembalian_buku(credentials: HTTPAuthorizationCredentials = Depends(security), db: SessionLocal = Depends(get_db)):
    token_payload = decode_access_token(credentials.credentials)
    user_id = int(token_payload['sub'])
    return kembalikan_buku(db, user_id)

# Endpoint untuk memeriksa apakah buku telat dikembalikan atau masih dalam peminjaman
@app.get('/cek-peminjaman/{buku_id}')
def cek_peminjaman(buku_id: int, db: SessionLocal = Depends(get_db)):
    peminjaman = db.query(Peminjaman).filter(Peminjaman.buku_id == buku_id).first()
    if not peminjaman:
        raise HTTPException(status_code=404, detail='Book not found')
    
    tanggal_pengembalian = peminjaman.tanggal_pengembalian
    if not tanggal_pengembalian:
        return {'status': 'Buku masih dalam peminjaman'}
    
    if tanggal_pengembalian < datetime.utcnow():
        return {'status': 'Buku telat dikembalikan'}
    
    return {'status': 'Buku sudah dikembalikan'}

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host='0.0.0.0', port=8000)
