from .db import SessionLocal

# Dependency untuk mendapatkan database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()