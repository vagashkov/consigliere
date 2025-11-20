from fastapi import APIRouter
from httpx import AsyncClient
from pydantic import ValidationError as PydanticError

from src.api.v1.app.utils import report_error

from src.api.v1.app.constants import (
    HTTPMethod,
    LIST_ALL_MODELS_URL, LIST_ACTIVE_MODELS_URL
)
from src.api.v1.app.models.service import LLModelsList


async def list_models(active: bool = False) -> LLModelsList:
    """
    Returns local LLMs list (all or active only)
    :return:
    """

    # Define necessary inference engine endpoint
    url = LIST_ACTIVE_MODELS_URL if active else LIST_ALL_MODELS_URL

    # Getting models list from inference engine
    try:
        async with AsyncClient() as client:
            response = await client.get(
                url
            )
    except Exception as e:
        report_error(str(e))

    models_list = response.json()

    # Validate received data
    try:
        LLModelsList.model_validate(
            models_list
        )
    except PydanticError as e:
        report_error(str(e))

    # Return result
    return LLModelsList(**models_list)


async def list_all_models() -> LLModelsList:
    """
    Returns all available LLMs (incl. aliases)
    :return:
    """

    return await list_models(active=False)


async def list_active_models() -> LLModelsList:
    """
    Returns active LLMs (incl. aliases)
    :return:
    """

    return await list_models(active=True)


router = APIRouter()

router.add_api_route(
    "/models",
    endpoint=list_all_models,
    methods=[HTTPMethod.GET],
    summary="Returns all available LLMs (incl. aliases)"
)
router.add_api_route(
    "/models/active",
    endpoint=list_active_models,
    methods=[HTTPMethod.GET],
    summary="Returns active LLMs only (incl. aliases)"
)
