from http import HTTPStatus
from fastapi.testclient import TestClient

from src.api.v1.main import app
from src.api.v1.routes.admin import get_llm_service
from tests.mock_objects import (
    ALL_LLM_MODELS, ACTIVE_LLM_MODELS, get_mock_llm_service
)

client = TestClient(app)

MODEL_NAME = "test_model"
MODEL_VERSION = "0.1.0"

def test_list_all_models():
    """
    Test the 'list all models' endpoint
    """
    app.dependency_overrides[get_llm_service] = get_mock_llm_service
    response = client.get("api/v1/admin/models")
    # Check response status code
    assert response.status_code == HTTPStatus.OK.value
    # Check response data
    data = response.json()
    # Check response data type
    assert isinstance(data, list)
    # Check response data length
    assert len(data) == len(ALL_LLM_MODELS)
    # Compare response data with LLM_MODELS content
    for model in data:
        assert model in ALL_LLM_MODELS
    for model in ALL_LLM_MODELS:
        assert model in data


def test_list_active_models():
    """
    Test the 'list active models' endpoint
    """
    app.dependency_overrides[get_llm_service] = get_mock_llm_service
    response = client.get("api/v1/admin/models/active")
    # Check response status code
    assert response.status_code == HTTPStatus.OK.value
    # Check response data
    data = response.json()
    # Check response data type
    assert isinstance(data, list)
    # Check response data length
    assert len(data) == len(ACTIVE_LLM_MODELS)
    # Compare response data with LLM_MODELS content
    for model in data:
        assert model in ACTIVE_LLM_MODELS
    for model in ACTIVE_LLM_MODELS:
        assert model in data


def test_pull_model():
    """
    Test the 'pull model' endpoint
    """

    app.dependency_overrides[get_llm_service] = get_mock_llm_service
    response = client.get(
        "api/v1/admin/models/pull/{}/{}".format(
            MODEL_NAME, MODEL_VERSION
        )
    )
    # Check response status code
    assert response.status_code == HTTPStatus.ACCEPTED.value
    # Check response data
    data = response.json()
    # Check response data type
    assert isinstance(data, dict)
    # Check response data length
    assert data == {
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION
    }


def test_delete_model():
    """
    Test the 'delete model' endpoint
    """

    app.dependency_overrides[get_llm_service] = get_mock_llm_service
    response = client.delete(
        "api/v1/admin/models/{}/{}".format(
            MODEL_NAME, MODEL_VERSION
        )
    )
    # Check response status code
    assert response.status_code == HTTPStatus.ACCEPTED.value
    # Check response data
    data = response.json()
    # Check response data type
    assert isinstance(data, dict)
    # Check response data length
    assert data == {
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION
    }

