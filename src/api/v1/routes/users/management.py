from fastapi import APIRouter, Depends, Path
from starlette import status
from typing import List

from src.constants import HTTPMethod
from src.core.models import UserRequestDTO, UserResponseDTO
from src.core.services.users.management import UserService
from src.data.storage.database.postgres import AsyncLocalSession
from src.dependencies import get_db_session


async def add_user(
        user_dto: UserRequestDTO,
        session: AsyncLocalSession = Depends(get_db_session)
) -> UserResponseDTO:
    """
    Adds new user
    :param user_dto:
    :param session:
    :return:
    """
    return await UserService(session).add_user(
        user_dto
    )


async def list_all_users(
        session: AsyncLocalSession = Depends(get_db_session)
        ) -> List[UserResponseDTO]:
    """
    Returns all users list
    :param session:
    :return:
    """

    return await UserService(session).list_all_users()


async def get_user_data(
        user_id: int = Path(gt=0),
        session: AsyncLocalSession = Depends(get_db_session)
        ) -> UserResponseDTO:
    """
    Gets designated user details
    :param user_id:
    :param session:
    :return:
    """

    return await UserService(session).get_user_data(
        user_id
    )


async def put_user_data(
        user_dto: UserRequestDTO,
        user_id: int = Path(gt=0),
        session: AsyncLocalSession = Depends(get_db_session)
        ) -> UserResponseDTO:
    """
    Updates designated user details
    :param user_dto:
    :param user_id:
    :param session:
    :return:
    """

    return await UserService(session).put_user_data(
        user_id,
        user_dto
    )


async def delete_user(
        user_id: int = Path(gt=0),
        session: AsyncLocalSession = Depends(get_db_session)
        ) -> None:
    """
    Deletes designated user details
    :param user_id:
    :param session:
    :return:
    """

    return await UserService(session).delete_user(
        user_id
    )


users_router = APIRouter(
    tags=["users"]
)

users_router.add_api_route(
    "/",
    endpoint=list_all_users,
    methods=[HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    summary="Returns all available user list"
)

users_router.add_api_route(
    "/",
    endpoint=add_user,
    methods=[HTTPMethod.POST],
    status_code=status.HTTP_201_CREATED,
    summary="Saves new User into database"
)

users_router.add_api_route(
    "/{user_id}",
    endpoint=get_user_data,
    methods=[HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    summary="Gets designated user details"
)

users_router.add_api_route(
    "/{user_id}",
    endpoint=put_user_data,
    methods=[HTTPMethod.PUT],
    status_code=status.HTTP_200_OK,
    summary="Updates designated User details"
)

users_router.add_api_route(
    "/{user_id}",
    endpoint=delete_user,
    methods=[HTTPMethod.DELETE],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletes designated user"
)
