from fastapi import APIRouter, Depends, Path
from starlette import status
from typing import List

from src.constants import HTTPMethod
from src.core.models import LLMRequestDTO, LLMResponseDTO
from src.core.services.llms import LLMService
from src.data.storage.database.postgres import AsyncLocalSession
from src.dependencies import get_db_session


async def add_llm(
        llm_dto: LLMRequestDTO,
        session: AsyncLocalSession = Depends(get_db_session)
) -> LLMResponseDTO:
    """
    Adds new LLM
    :param llm_dto:
    :param session:
    :return:
    """
    return await LLMService(session).add_llm(
        llm_dto
    )


async def list_all_llms(
        session: AsyncLocalSession = Depends(get_db_session)
        ) -> List[LLMResponseDTO]:
    """
    Returns all LLMs list
    :param session:
    :return:
    """

    return await LLMService(session).list_all_llms()


async def get_llm_data(
        llm_id: int = Path(gt=0),
        session: AsyncLocalSession = Depends(get_db_session)
        ) -> LLMResponseDTO:
    """
    Gets designated LLM details
    :param llm_id:
    :param session:
    :return:
    """

    return await LLMService(session).get_llm_data(
        llm_id
    )


async def put_llm_data(
        llm_dto: LLMRequestDTO,
        llm_id: int = Path(gt=0),
        session: AsyncLocalSession = Depends(get_db_session)
        ) -> LLMResponseDTO:
    """
    Updates designated LLM details
    :param llm_dto:
    :param llm_id:
    :param session:
    :return:
    """

    return await LLMService(session).put_llm_data(
        llm_id,
        llm_dto
    )


async def delete_llm(
        llm_id: int = Path(gt=0),
        session: AsyncLocalSession = Depends(get_db_session)
        ) -> None:
    """
    Deletes designated LLM details
    :param llm_id:
    :param session:
    :return:
    """

    return await LLMService(session).delete_llm(
        llm_id
    )


llm_admin_router = APIRouter()

llm_admin_router.add_api_route(
    "/",
    endpoint=list_all_llms,
    methods=[HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    summary="Returns all available LLM list"
)

llm_admin_router.add_api_route(
    "/",
    endpoint=add_llm,
    methods=[HTTPMethod.POST],
    status_code=status.HTTP_201_CREATED,
    summary="Saves new LLM into database"
)

llm_admin_router.add_api_route(
    "/{llm_id}",
    endpoint=get_llm_data,
    methods=[HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    summary="Gets designated LLM details"
)

llm_admin_router.add_api_route(
    "/{llm_id}",
    endpoint=put_llm_data,
    methods=[HTTPMethod.PUT],
    status_code=status.HTTP_200_OK,
    summary="Updates designated LLM details"
)

llm_admin_router.add_api_route(
    "/{llm_id}",
    endpoint=delete_llm,
    methods=[HTTPMethod.DELETE],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletes designated LLM"
)
