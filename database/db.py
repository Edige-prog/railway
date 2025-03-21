from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# "postgresql+psycopg2://store_user:SomePassword123@localhost/flowers_db"
SQLALCHEMY_DATABASE_URL = os.environ['DB_URL']

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_tables():
    Base.metadata.create_all(bind=engine)