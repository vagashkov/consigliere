from fastapi import APIRouter
from typing import List


from src.constants import HTTPMethod
from src.core.models import LLModelDTO
from src.core.services import LLMService


async def list_all_models() -> List[LLModelDTO]:
    """
    Returns all available LLMs (incl. aliases)
    :return:
    """

    return await LLMService().list_models()


async def list_active_models() -> List[LLModelDTO]:
    """
    Returns active LLMs (incl. aliases)
    :return:
    """

    return await LLMService().list_models(active=True)


async def pull_model(
        model_name: str,
        model_version: str
):
    """
    Initiate pulling of a model with specified name and version
    :return:
    """

    return await LLMService().pull_model(model_name, model_version)


async def delete_model(
        model_name: str,
        model_version: str
):
    """
    Initiate pulling of a model with specified name and version
    :return:
    """

    return await LLMService().delete_model(model_name, model_version)


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
router.add_api_route(
    "/models/pull/{model_name}/{model_version}",
    endpoint=pull_model,
    methods=[HTTPMethod.GET],
    summary="Pulls a model with specified name and version"
)
router.add_api_route(
    "/models/{model_name}/{model_version}",
    endpoint=delete_model,
    methods=[HTTPMethod.DELETE],
    summary="Deletes a model with specified name and version"
)
