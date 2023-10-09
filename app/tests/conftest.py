# from celery import current_app
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def non_mocked_hosts() -> list:
    return ["testserver"]

