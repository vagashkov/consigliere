from fastapi import HTTPException
from http import HTTPStatus
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError
from typing import List

from src.core.models import LLMProviderRequestDTO, LLMProviderResponseDTO
from src.core.services.base import DBEnabledService
from src.data.storage.database.models import LLMProvider


class LLMProvidersService(DBEnabledService):
    """"
    Manages LLM providers (both local and external) lifecycle
    """

    async def add_llm_provider(
            self,
            provider_dto: LLMProviderRequestDTO
    ) -> LLMProviderResponseDTO:
        """
        Adds new LLM provider
        :param provider_dto:
        :return:
        """

        # Build model object instance
        provider: LLMProvider = LLMProvider(**provider_dto.model_dump())

        try:
            # Add object to session and save it to database
            self.session.add(provider)
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
            return LLMProviderResponseDTO.model_validate(provider)
        except ValidationError as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database object validation error: {e}"
            )

    async def list_all_llm_providers(self) -> List[LLMProviderResponseDTO]:
        """
        Returns all LLM providers (incl. non-active)
        :return:
        """
        #
        try:
            providers_list = await self.session.scalars(select(LLMProvider))
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
                LLMProviderResponseDTO.model_validate(provider)
                for provider
                in providers_list.all()
                ]
        except ValidationError as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database object validation error: {e}"
            )

    async def get_llm_provider_data(
            self, provider_id: int
    ) -> LLMProviderResponseDTO:
        """
        Returns all LLM providers (incl. non-active)
        :return:
        """
        #
        try:
            provider: LLMProvider = await self.session.scalar(
                select(LLMProvider).filter(
                    LLMProvider.id == provider_id
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
        if not provider:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"LLM provider with {provider_id} ID is not found"
            )

        # Return result
        try:
            return LLMProviderResponseDTO.model_validate(provider)
        except ValidationError as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database object validation error: {e}"
            )

    async def put_llm_provider_data(
            self, provider_id: int, provider_dto: LLMProviderRequestDTO
    ) -> LLMProviderResponseDTO:
        """
        Returns all LLM providers (incl. non-active)
        :return:
        """
        #
        try:
            provider: LLMProvider = await self.session.scalar(
                select(LLMProvider).filter(
                    LLMProvider.id == provider_id
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
        if not provider:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"LLM provider with {provider_id} ID is not found"
            )

        # Update provider object data
        provider.name = provider_dto.name
        provider.url = provider_dto.url
        provider.port = provider_dto.port
        provider.description = provider_dto.description

        try:
            # Add object to session and save it to database
            self.session.add(provider)
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
            return LLMProviderResponseDTO.model_validate(provider)
        except ValidationError as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database object validation error: {e}"
            )

    async def delete_llm_provider(self, provider_id: int) -> None:
        """
        Returns all LLM providers (incl. non-active)
        :return:
        """
        # Getting designated provider object
        try:
            provider: LLMProvider = await self.session.scalar(
                select(LLMProvider).filter(
                    LLMProvider.id == provider_id
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
        if not provider:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"LLM provider with {provider_id} ID is not found"
            )

        try:
            # Add object to session and save it to database
            await self.session.delete(provider)
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
