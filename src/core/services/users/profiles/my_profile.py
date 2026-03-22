from fastapi import HTTPException
from http import HTTPStatus

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import OperationalError

from src.core.services.base import DBEnabledService
from src.core.models import UserResponseDTO
from src.data.storage.database.models import User


class MyProfileService(DBEnabledService):
    """
    Manages user profile lifecycle
    """

    async def get_my_user_data(
            self,
            user_data: dict
            ) -> UserResponseDTO:
        """
        User password change routine
        :param user_data:
        :return:
        """

        # Checking user credentials
        if not user_data:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid access token"
            )

        # Looking for user by email
        try:
            user_object: User = await self.session.scalar(
                select(User).filter(
                    User.email == user_data.get("email")
                ).limit(1)
            )
        except OperationalError as e:
            # raise a relevant HTTPException
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database error: {e}"
            )
        except Exception as e:
            # Handle other unexpected exceptions
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {e}"
            )

        # Check if user is found
        if not user_object:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"User {user_data.get('email')} not found"
            )

        # Return result
        try:
            return UserResponseDTO.model_validate(user_object)
        except ValidationError as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database object validation error: {e}"
            )
