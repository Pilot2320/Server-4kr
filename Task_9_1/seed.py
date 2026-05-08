from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Product

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed():
    db = SessionLocal()
    p1 = Product(title="Laptop", price=1000.0, count=5)
    p2 = Product(title="Mouse", price=25.0, count=50)
    db.add(p1)
    db.add(p2)
    db.commit()
    db.close()
    print("Seed data added.")

if __name__ == "__main__":
    seed()
