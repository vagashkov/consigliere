from fastapi import APIRouter, Depends
from typing import List


from src.api.v1.dependencies import LLMServiceDependency
from src.constants import HTTPMethod
from src.core.models import LLModelDTO
from src.core.services import LLMService


async def list_all_models(
        llm_service: LLMService = Depends(
            LLMServiceDependency.get_llm_service
        )
) -> List[LLModelDTO]:
    """
    Returns all available LLMs (incl. aliases)
    :return:
    """

    return await llm_service.list_models()


async def list_active_models(
    llm_service: LLMService = Depends(
        LLMServiceDependency.get_llm_service
    )
) -> List[LLModelDTO]:
    """
    Returns active LLMs (incl. aliases)
    :return:
    """

    return await llm_service.list_models(active=True)


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
