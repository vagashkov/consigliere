from fastapi import APIRouter, Depends, Path
from starlette import status
from typing import List

from src.constants import HTTPMethod
from src.core.models import LLMProviderRequestDTO, LLMProviderResponseDTO
from src.core.services.llm_providers import LLMProvidersService
from src.data.storage.database.postgres import AsyncLocalSession
from src.dependencies import get_db_session


async def add_llm_provider(
        provider_dto: LLMProviderRequestDTO,
        session: AsyncLocalSession = Depends(get_db_session)
) -> LLMProviderResponseDTO:
    """
    Adds new LLM provider
    :param provider_dto:
    :param session:
    :return:
    """
    return await LLMProvidersService(session).add_llm_provider(
        provider_dto
    )


async def list_all_llm_providers(
        session: AsyncLocalSession = Depends(get_db_session)
        ) -> List[LLMProviderResponseDTO]:
    """
    Returns all LLM providers data
    :param session:
    :return:
    """

    return await LLMProvidersService(session).list_all_llm_providers()


async def get_llm_provider_data(
        provider_id: int = Path(gt=0),
        session: AsyncLocalSession = Depends(get_db_session)
        ) -> LLMProviderResponseDTO:
    """
    Gets designated LLM provider details
    :param provider_id:
    :param session:
    :return:
    """

    return await LLMProvidersService(session).get_llm_provider_data(
        provider_id
    )


async def put_llm_provider_data(
        provider_dto: LLMProviderRequestDTO,
        provider_id: int = Path(gt=0),
        session: AsyncLocalSession = Depends(get_db_session)
        ) -> LLMProviderResponseDTO:
    """
    Updates designated LLM provider details
    :param provider_dto:
    :param provider_id:
    :param session:
    :return:
    """

    return await LLMProvidersService(session).put_llm_provider_data(
        provider_id,
        provider_dto
    )


async def delete_llm_provider(
        provider_id: int = Path(gt=0),
        session: AsyncLocalSession = Depends(get_db_session)
        ) -> None:
    """
    Deletes designated LLM provider details
    :param provider_id:
    :param session:
    :return:
    """

    return await LLMProvidersService(session).delete_llm_provider(
        provider_id
    )


llm_providers_admin_router = APIRouter()

llm_providers_admin_router.add_api_route(
    "/",
    endpoint=list_all_llm_providers,
    methods=[HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    summary="Returns all available LLM providers"
)

llm_providers_admin_router.add_api_route(
    "/",
    endpoint=add_llm_provider,
    methods=[HTTPMethod.POST],
    status_code=status.HTTP_201_CREATED,
    summary="Saves new LLM provider into database"
)

llm_providers_admin_router.add_api_route(
    "/{provider_id}",
    endpoint=get_llm_provider_data,
    methods=[HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    summary="Gets designated LLM provider details"
)

llm_providers_admin_router.add_api_route(
    "/{provider_id}",
    endpoint=put_llm_provider_data,
    methods=[HTTPMethod.PUT],
    status_code=status.HTTP_200_OK,
    summary="Updates designated LLM provider details"
)

llm_providers_admin_router.add_api_route(
    "/{provider_id}",
    endpoint=delete_llm_provider,
    methods=[HTTPMethod.DELETE],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletes designated LLM provider"
)
