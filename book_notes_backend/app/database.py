from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

if os.getenv("ENV") == "test":
    load_dotenv(".env.test")
else:
    load_dotenv(".env")

DATABASE_URL = str(os.environ.get("DATABASE_URL"))

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
