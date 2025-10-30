# app/database.py
from sqlmodel import SQLModel, create_engine, Session
import os

# Ensure directory exists
DATA_DIR = "/code/app/data"
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_URL = f"sqlite:///{DATA_DIR}/budget.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session