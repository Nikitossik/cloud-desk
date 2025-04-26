import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.models import Application
from app.database import Base
from app.dependencies.database import get_db
from main import app
from .utils import auth_headers

from uuid import UUID

TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    yield client


@pytest.fixture(scope="session")
def user_token(client):
    register_data = {
        "name": "Test",
        "surname": "Test",
        "email": "testuser@gmail.com",
        "password": "testpassword",
    }
    client.post("/auth/signup", json=register_data)

    response = client.post(
        "/auth/token",
        data={
            "username": register_data["email"],
            "password": register_data["password"],
        },
    )
    tokens = response.json()

    return tokens["access_token"]


@pytest.fixture()
def test_device(client, user_token):
    response: Response = client.get("/device", headers=auth_headers(user_token))
    return response.json()


@pytest.fixture()
def test_applications(db, test_device):
    test_apps = [
        {
            "name": "TestApp1.exe",
            "exe": "C://some/where/on/the/disk/TestApp1.exe",
            "cmdline": "",
            "device_id": UUID(test_device["id"]),
        },
        {
            "name": "TestApp2.exe",
            "exe": "C://some/where/on/the/disk/TestApp2.exe",
            "cmdline": "",
            "device_id": UUID(test_device["id"]),
        },
    ]

    db_apps = [Application(**test_app) for test_app in test_apps]

    for db_app in db_apps:
        db.add(db_app)

    db.commit()

    for db_app in db_apps:
        db.refresh(db_app)

    return db_apps
