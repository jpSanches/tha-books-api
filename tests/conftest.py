import os
import tempfile
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.db.models import Base
from app.db.deps import get_db
from app.main import app

# Use temporary SQLite DB for fast, isolated testing
db_fd, db_path = tempfile.mkstemp(suffix=".db")
SQLALCHEMY_TEST_URL = f"sqlite:///{db_path}"

engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fixture that provides a clean DB session for each test
@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    if os.path.exists("test.db"):
        os.remove("test.db")

    Base.metadata.create_all(bind=engine)
    session: Session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# Override get_db dependency with test DB session
@pytest.fixture(scope="function", autouse=True)
def override_get_db(db: Session):
    def _get_test_db() -> Generator[Session, None, None]:
        yield db

    app.dependency_overrides[get_db] = _get_test_db


# Reusable FastAPI test client
@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


# Reusable login token fixture
@pytest.fixture(scope="function")
def auth_token(client: TestClient) -> str:
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    secret_key = os.getenv("SECRET_KEY")

    assert secret_key, "SECRET_KEY must be set"
    assert username and password, "ADMIN_USERNAME and ADMIN_PASSWORD must be set"

    response = client.post(
        "/v1/auth/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    return response.json()["access_token"]


# Helper to generate auth headers
@pytest.fixture
def auth_headers(auth_token: str) -> dict:
    return {"Authorization": f"Bearer {auth_token}"}
