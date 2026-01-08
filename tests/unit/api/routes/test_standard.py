from http import HTTPStatus
from fastapi.testclient import TestClient
import pytest

from src.api.v1.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_health_check():
    """
    Test the health check endpoint
    """
    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK.value
    data = response.json()
    assert isinstance(data, dict)
    assert "status" in data
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_index_page():
    """
    Test the index page retrieval
    """
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK.value
    assert "text/html" in response.headers["content-type"]
    # Assert content based on the expected template.
    with open("static/templates/index.html", "r", encoding="utf-8") as f:
        template_content = f.read()
    assert response.text.strip() in template_content.strip()
