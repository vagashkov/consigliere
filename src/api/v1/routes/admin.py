from fastapi import APIRouter, Depends
from starlette import status
from typing import List


from src.constants import HTTPMethod
from src.dependencies import get_llm_service
from src.core.models import LLModelDTO
from src.core.services.llm import LLMService


async def list_all_models(
        llm_service: LLMService = Depends(get_llm_service)
) -> List[LLModelDTO]:
    """
    Returns all available LLMs (incl. aliases)
    :return:
    """

    return await llm_service.list_models()


async def list_active_models(
        llm_service: LLMService = Depends(get_llm_service)
) -> List[LLModelDTO]:
    """
    Returns active LLMs (incl. aliases)
    :return:
    """

    return await llm_service.list_models(active=True)


async def pull_model(
        model_name: str,
        model_version: str,
        llm_service: LLMService = Depends(get_llm_service)
):
    """
    Initiate pulling of a model with specified name and version
    :return:
    """

    return await llm_service.pull_model(model_name, model_version)


async def delete_model(
        model_name: str,
        model_version: str,
        llm_service: LLMService = Depends(get_llm_service)
):
    """
    Initiate pulling of a model with specified name and version
    :return:
    """

    return await llm_service.delete_model(model_name, model_version)


router = APIRouter()

router.add_api_route(
    "/models",
    endpoint=list_all_models,
    methods=[HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    summary="Returns all available LLMs (incl. aliases)"
)
router.add_api_route(
    "/models/active",
    endpoint=list_active_models,
    methods=[HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    summary="Returns active LLMs only (incl. aliases)"
)
router.add_api_route(
    "/models/pull/{model_name}/{model_version}",
    endpoint=pull_model,
    methods=[HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    summary="Pulls a model with specified name and version"
)
router.add_api_route(
    "/models/{model_name}/{model_version}",
    endpoint=delete_model,
    methods=[HTTPMethod.DELETE],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletes a model with specified name and version"
)
