import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
from fastapi.testclient import TestClient
import os
from app import database
from dotenv import load_dotenv


if os.getenv("ENV") == "test":
    load_dotenv(".env.test")
else:
    load_dotenv(".env")

TEST_DATABASE_URL = str(os.getenv("DATABASE_URL"))

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override DB dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[database.SessionLocal] = override_get_db

@pytest.fixture()
def client():
    return TestClient(app)
