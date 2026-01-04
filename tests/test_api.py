from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from magrathea.database import Base, get_db
from magrathea.main import app

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session() -> Generator[Session]:
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient]:
    def override_get_db() -> Generator[Session]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_create_and_get_map(client: TestClient) -> None:
    # 1. Create a map
    response = client.post("/maps", json={"size": 64, "octaves": 2})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "url" in data

    map_url = data["url"]

    # 2. Retrieve the map
    response = client.get(map_url)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert len(response.content) > 0


def test_get_nonexistent_map(client: TestClient) -> None:
    response = client.get("/maps/nonexistent-id")
    assert response.status_code == 404


def test_create_map_with_density(client: TestClient) -> None:
    response = client.post(
        "/maps", json={"size": 64, "octaves": 2, "island_density": 0.5}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "url" in data


def test_quick_generate_map(client: TestClient) -> None:
    response = client.get("/map?size=64&octaves=2")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert len(response.content) > 0


def test_favicon(client: TestClient) -> None:
    response = client.get("/favicon.ico")
    assert response.status_code == 200
    assert response.headers["content-type"] in [
        "image/vnd.microsoft.icon",
        "image/x-icon",
    ]
