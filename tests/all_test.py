import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from main import app
from models.all_models import User, Buku, Peminjaman
from utils.helpers import register_user
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Test for register function
def test_register(db: Session):
    user_data = {'email': 'testuser@example.com', 'password': 'password123'}
    response = app.post('/register', json=user_data)
    assert response.status_code == 200
    assert response.json() == 1
    # Test for registering with existing email
    response = app.post('/register', json=user_data)
    assert response.status_code == 400
# Test for login function
def test_login(db: Session):
    user_data = {'email': 'testuser@example.com', 'password': 'password123'}
    register_user(db, user_data['email'], user_data['password'])
    # Test for successful login
    response = app.post('/login', json=user_data)
    assert response.status_code == 200
    assert 'access_token' in response.json()
    # Test for incorrect email
    user_data['email'] = 'wrongemail@example.com'
    response = app.post('/login', json=user_data)
    assert response.status_code == 400
    # Test for incorrect password
    user_data['email'] = 'testuser@example.com'
    user_data['password'] = 'wrongpassword'
    response = app.post('/login', json=user_data)
    assert response.status_code == 400
# Test for peminjaman_buku function
def test_peminjaman_buku(db: Session):
    # Create a user and a book
    user = User(email='testuser@example.com', password=pwd_context.hash('password123'))
    db.add(user)
    db.commit()
    buku = Buku(judul='Test Book', pengarang='Test Author', penerbit='Test Publisher', tahun_terbit=2021)
    db.add(buku)
    db.commit()
    # Test for successful peminjaman
    access_token = pwd_context.hash(json.dumps({'sub': user.id, 'role': 'user'}))
    headers = {'Authorization': f'Bearer {access_token}'}
    peminjaman_data = {'buku_id': buku.id}
    response = app.post('/peminjaman', json=peminjaman_data, headers=headers)
    assert response.status_code == 200
    assert response.json()['user_id'] == user.id
    assert response.json()['buku_id'] == buku.id
    # Test for peminjaman by non-admin user who already borrowed a book
    response = app.post('/peminjaman', json=peminjaman_data, headers=headers)
    assert response.status_code == 400
    # Test for peminjaman by admin user
    access_token = pwd_context.hash(json.dumps({'sub': user.id, 'role': 'admin'}))
    headers = {'Authorization': f'Bearer {access_token}'}
    response = app.post('/peminjaman', json=peminjaman_data, headers=headers)
    assert response.status_code == 200
# Test for pengembalian_buku function
def test_pengembalian_buku(db: Session):
    # Create a user and a book
    user = User(email='testuser@example.com', password=pwd_context.hash('password123'))
    db.add(user)
    db.commit()
    buku = Buku(judul='Test Book', pengarang='Test Author', penerbit='Test Publisher', tahun_terbit=2021)
    db.add(buku)
    db.commit()
    # Create a peminjaman
    peminjaman = Peminjaman(user_id=user.id, buku_id=buku.id, tanggal_peminjaman=datetime.utcnow())
    db.add(peminjaman)
    db.commit()
    # Test for successful pengembalian
    access_token = pwd_context.hash(json.dumps({'sub': user.id, 'role': 'user'}))
    headers = {'Authorization': f'Bearer {access_token}'}
    response = app.post('/pengembalian', headers=headers)
    assert response.status_code == 200
    assert response.json()['user_id'] == user.id
    assert response.json()['buku_id'] == buku.id
    assert response.json()['tanggal_pengembalian'] is not None
    # Test for pengembalian by non-admin user who did not borrow a book
    response = app.post('/pengembalian', headers=headers)
    assert response.status_code == 400
    # Test for pengembalian by admin user
    access_token = pwd_context.hash(json.dumps({'sub': user.id, 'role': 'admin'}))
    headers = {'Authorization': f'Bearer {access_token}'}
    response = app.post('/pengembalian', headers=headers)
    assert response.status_code == 200
# Test for cek_peminjaman function
def test_cek_peminjaman(db: Session):
    # Create a user and a book
    user = User(email='testuser@example.com', password=pwd_context.hash('password123'))
    db.add(user)
    db.commit()
    buku = Buku(judul='Test Book', pengarang='Test Author', penerbit='Test Publisher', tahun_terbit=2021)
    db.add(buku)
    db.commit()
    # Test for book not found
    response = app.get('/cek-peminjaman/999')
    assert response.status_code == 404
    # Test for book still in peminjaman
    peminjaman = Peminjaman(user_id=user.id, buku_id=buku.id, tanggal_peminjaman=datetime.utcnow())
    db.add(peminjaman)
    db.commit()
    response = app.get(f'/cek-peminjaman/{buku.id}')
    assert response.status_code == 200
    assert response.json()['status'] == 'Buku masih dalam peminjaman'
    # Test for book returned on time
    peminjaman.tanggal_pengembalian = datetime.utcnow()
    db.commit()
    response = app.get(f'/cek-peminjaman/{buku.id}')
    assert response.status_code == 200
    assert response.json()['status'] == 'Buku sudah dikembalikan'
    # Test for book returned late
    peminjaman.tanggal_pengembalian = datetime.utcnow() - timedelta(days=1)
    db.commit()
    response = app.get(f'/cek-peminjaman/{buku.id}')
    assert response.status_code == 200
    assert response.json()['status'] == 'Buku telat dikembalikan'