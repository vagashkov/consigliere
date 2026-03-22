from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.constants import HTTPMethod
from src.core.models import AccessToken, ChangePasswordRequestDTO
from src.core.services.users.auth import AuthService, get_current_user
from src.data.storage.database.postgres import AsyncLocalSession
from src.dependencies import get_db_session


async def login(
        form_data: OAuth2PasswordRequestForm = Depends(
            OAuth2PasswordRequestForm
        ),
        session: AsyncLocalSession = Depends(
            get_db_session
        )
) -> AccessToken:
    return await AuthService(session).login(form_data)


async def change_password(
        passwords: ChangePasswordRequestDTO,
        user: dict = Depends(get_current_user),
        session: AsyncLocalSession = Depends(get_db_session)
) -> dict:
    return await AuthService(session).change_password(
        user, passwords
    )

auth_router = APIRouter(
    tags=["auth"]
)

auth_router.add_api_route(
    "/login",
    endpoint=login,
    methods=[HTTPMethod.POST],
    status_code=status.HTTP_200_OK,
    summary="User login endpoint"
)

auth_router.add_api_route(
    "/password",
    endpoint=change_password,
    methods=[HTTPMethod.POST],
    status_code=status.HTTP_200_OK,
    summary="User change password endpoint"
)
