from fastapi import HTTPException
from http import HTTPStatus
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError
from typing import List


from src.core.models import UserRequestDTO, UserResponseDTO
from src.core.services.base import DBEnabledService
from src.data.storage.database.models import User


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(DBEnabledService):
    """"
    Manages users lifecycle
    """

    async def add_user(
            self,
            user_dto: UserRequestDTO
    ) -> UserResponseDTO:
        """
        Adds new user
        :param user_dto:
        :return:
        """

        # Build model object instance
        user_object: User = User(
            email=user_dto.email,
            password_hash=bcrypt_context.hash(user_dto.password),
            role=user_dto.role,
            is_active=True
            )

        try:
            # Add object to session and save it to database
            self.session.add(user_object)
            await self.session.commit()
        except IntegrityError as e:
            # Handle integrity errors (e.g., duplicate key)
            await self.session.rollback()
            # raise a relevant HTTPException
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Data integrity error: {e}"
            )
        except (OperationalError, ProgrammingError) as e:
            # Handle connection or SQL errors
            await self.session.rollback()
            # raise a relevant HTTPException
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database error: {e}"
            )
        except Exception as e:
            # Handle other unexpected exceptions
            await self.session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {e}"
            )

        # Return newly created object
        try:
            return UserResponseDTO.model_validate(user_object)
        except ValidationError as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database object validation error: {e}"
            )

    async def list_all_users(self) -> List[UserResponseDTO]:
        """
        Returns all users list
        :return:
        """
        #
        try:
            users_list = await self.session.scalars(select(User))
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

        try:
            return [
                UserResponseDTO.model_validate(user_object)
                for user_object
                in users_list.all()
                ]
        except ValidationError as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database object validation error: {e}"
            )

    async def get_user_data(
            self, user_id: int
    ) -> UserResponseDTO:
        """
        Returns user details
        :return:
        """
        #
        try:
            user_object: User = await self.session.scalar(
                select(User).filter(
                    User.id == user_id
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

        # Check if provider is found
        if not user_object:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"user with {user_id} ID is not found"
            )

        # Return result
        try:
            return UserResponseDTO.model_validate(user_object)
        except ValidationError as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database object validation error: {e}"
            )

    async def put_user_data(
            self, user_id: int, user_dto: UserRequestDTO
    ) -> UserResponseDTO:
        """
        Updates user details
        :param: user_id
        :param: user_dto
        :return:
        """
        # Getting user object from database
        try:
            user_object: User = await self.session.scalar(
                select(User).filter(
                    User.id == user_id
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

        # Check if provider is found
        if not user_object:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"user provider with {user_id} ID is not found"
            )

        # Update provider object data
        user_object.role = user_dto.role

        try:
            # Add object to session and save it to database
            self.session.add(user_object)
            await self.session.commit()
        except IntegrityError as e:
            # Handle integrity errors (e.g., duplicate key)
            await self.session.rollback()
            # raise a relevant HTTPException
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Data integrity error: {e}"
            )
        except (OperationalError, ProgrammingError) as e:
            # Handle connection or SQL errors
            await self.session.rollback()
            # raise a relevant HTTPException
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database error: {e}"
            )
        except Exception as e:
            # Handle other unexpected exceptions
            await self.session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {e}"
            )

        # Return updated object
        try:
            return UserResponseDTO.model_validate(user_object)
        except ValidationError as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database object validation error: {e}"
            )

    async def delete_user(self, user_id: int) -> None:
        """
        Deletes user data from database
        :param: user_id
        :return:
        """
        # Getting user object from database
        try:
            user_object: User = await self.session.scalar(
                select(User).filter(
                    User.id == user_id
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

        # Check if provider is found
        if not user_object:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"user with {user_id} ID is not found"
            )

        try:
            # Add object to session and save it to database
            await self.session.delete(user_object)
            await self.session.commit()
        except IntegrityError as e:
            # Handle integrity errors (e.g., duplicate key)
            await self.session.rollback()
            # raise a relevant HTTPException
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Data integrity error: {e}"
            )
        except (OperationalError, ProgrammingError) as e:
            # Handle connection or SQL errors
            await self.session.rollback()
            # raise a relevant HTTPException
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database error: {e}"
            )
        except Exception as e:
            # Handle other unexpected exceptions
            await self.session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {e}"
            )
