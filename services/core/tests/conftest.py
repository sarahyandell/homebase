import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tasks.api import get_repository
from app.tasks.repository import InMemoryTaskRepository


@pytest.fixture
def client():
    repo = InMemoryTaskRepository()
    app.dependency_overrides[get_repository] = lambda: repo
    yield TestClient(app)
    app.dependency_overrides.clear()
