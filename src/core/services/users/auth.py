from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from http import HTTPStatus

from fastapi import Depends
from fastapi.security import (
    OAuth2PasswordRequestForm, OAuth2PasswordBearer
)
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import OperationalError

from src.config import settings
from src.core.services.base import DBEnabledService
from src.core.models import AccessToken
from src.data.storage.database.models import User


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
        access_token: str = Depends(oauth2_bearer)
) -> dict:
    """
    Access token decode routine
    :param access_token:
    :return:
    """

    try:
        # Decode payload from token
        payload = jwt.decode(
            access_token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.JWT_ALGORITHM]
        )

        # Extract user id and email
        user_email: str = payload.get("sub")
        user_id: str = payload.get("id")

        # If no email/id - return error
        if not user_email or not user_id:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid access token"
            )

        # Return user data
        return {
            "id": user_id,
            "email": user_email
        }
    except JWTError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid access token"
        )


class AuthService(DBEnabledService):
    """
    Manages user sessions lifecycle
    """

    async def login(
            self,
            form_data: OAuth2PasswordRequestForm = Depends(
                OAuth2PasswordRequestForm
                )
            ) -> AccessToken:
        """
        User login routine
        :param form_data:
        :return:
        """

        # Looking for user by email
        try:
            user_object: User = await self.session.scalar(
                select(User).filter(
                    User.email == form_data.username
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
                detail=f"User {form_data.username} not found"
            )

        # Password hashes comparison
        if not bcrypt_context.verify(
            form_data.password, user_object.password_hash
        ):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Incorrect password"
            )

        # Build JWT payload
        encode = {
            "sub": user_object.email,
            "id": user_object.id,
            "exp": datetime.now(timezone.utc) + timedelta(
                seconds=settings.JWT_DURATION
            )
        }

        token_value = jwt.encode(
            encode,
            settings.SECRET_KEY.get_secret_value(),
            algorithm=settings.JWT_ALGORITHM
        )

        # Return JWT
        return AccessToken.model_validate(
            {
                "token_type": "bearer",
                "access_token": token_value
            }
        )
