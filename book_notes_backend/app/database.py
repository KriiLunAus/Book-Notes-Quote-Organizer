from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv()

user = os.environ.get("DB_USER")
password = os.environ.get("DB_USER_PASSWORD")

DATABASE_URL = f"postgresql://{user}:{password}@localhost/book_notes"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
