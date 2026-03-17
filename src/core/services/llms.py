from fastapi import HTTPException
from http import HTTPStatus
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError
from typing import List

from src.core.models import LLMRequestDTO, LLMResponseDTO
from src.core.services.base import DBEnabledService
from src.data.storage.database.models import LLModel


class LLMService(DBEnabledService):
    """"
    Manages LL models (both local and remote) lifecycle
    """

    async def add_llm(
            self,
            llm_dto: LLMRequestDTO
    ) -> LLMResponseDTO:
        """
        Adds new LLM
        :param llm_dto:
        :return:
        """

        # Build model object instance
        llm: LLModel = LLModel(**llm_dto.model_dump())

        try:
            # Add object to session and save it to database
            self.session.add(llm)
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
            return LLMResponseDTO.model_validate(llm)
        except ValidationError as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database object validation error: {e}"
            )

    async def list_all_llms(self) -> List[LLMResponseDTO]:
        """
        Returns all LLMs
        :return:
        """
        #
        try:
            llms_list = await self.session.scalars(select(LLModel))
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
                LLMResponseDTO.model_validate(llm)
                for llm
                in llms_list.all()
                ]
        except ValidationError as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database object validation error: {e}"
            )

    async def get_llm_data(
            self, llm_id: int
    ) -> LLMResponseDTO:
        """
        Returns LLM details
        :return:
        """
        #
        try:
            llm: LLModel = await self.session.scalar(
                select(LLModel).filter(
                    LLModel.id == llm_id
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
        if not llm:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"LLM provider with {llm_id} ID is not found"
            )

        # Return result
        try:
            return LLMResponseDTO.model_validate(llm)
        except ValidationError as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database object validation error: {e}"
            )

    async def put_llm_data(
            self, llm_id: int, llm_dto: LLMRequestDTO
    ) -> LLMResponseDTO:
        """
        Updates LLM details
        :param: llm_id
        :param: llm_dto
        :return:
        """
        # Getting LLM object from database
        try:
            llm: LLModel = await self.session.scalar(
                select(LLModel).filter(
                    LLModel.id == llm_id
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
        if not llm:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"LLM provider with {llm_id} ID is not found"
            )

        # Update provider object data
        llm.name = llm_dto.name
        llm.size = llm_dto.size
        llm.format = llm_dto.format
        llm.parameters = llm_dto.parameters
        llm.quantization_level = llm_dto.quantization_level

        try:
            # Add object to session and save it to database
            self.session.add(llm)
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
            return LLMResponseDTO.model_validate(llm)
        except ValidationError as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Database object validation error: {e}"
            )

    async def delete_llm(self, llm_id: int) -> None:
        """
        Deletes LLM data from database
        :param: llm_id
        :return:
        """
        # Getting LLM object from database
        try:
            llm: LLModel = await self.session.scalar(
                select(LLModel).filter(
                    LLModel.id == llm_id
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
        if not llm:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"LLM with {llm_id} ID is not found"
            )

        try:
            # Add object to session and save it to database
            await self.session.delete(llm)
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
