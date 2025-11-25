from fastapi import APIRouter, Depends


from src.api.v1.app.dependencies import LLMServiceDependency
from src.api.v1.app.constants import HTTPMethod
from src.api.v1.app.models.service import LLModelsList
from src.api.v1.app.services.service import LLMService


async def list_all_models(
        llm_service: LLMService = Depends(
            LLMServiceDependency.get_llm_service
        )
) -> LLModelsList:
    """
    Returns all available LLMs (incl. aliases)
    :return:
    """

    return await llm_service.list_models()


async def list_active_models(
    llm_service: LLMService = Depends(
        LLMServiceDependency.get_llm_service
    )
) -> LLModelsList:
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
