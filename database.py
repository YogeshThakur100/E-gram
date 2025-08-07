from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

home_path = os.path.expanduser("~")
print(home_path)
database_path = os.path.join(home_path , 'Databasessqllite')
os.makedirs(database_path , exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_path}/grampanchayat.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



Base = declarative_base()

Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()