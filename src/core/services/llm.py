from http import HTTPStatus
from typing import List

from fastapi import HTTPException

import src.dependencies as dependencies
from src.core.models import LLModelDTO
from src.core.services.validator import prompt_validator


class LLMService:
    """
    LLM service implementation
    """

    def __init__(self):
        super().__init__()
        self.client = dependencies.get_llm_client()

    async def list_models(self, active: bool = False) -> List[LLModelDTO]:
        """
        List all available models.
        :param active:
        :return:
        """
        return await self.client.list_models(active)

    async def pull_model(self, model_name: str, model_version: str):
        """
        Initiate pulling of a model from ollama models.
        :param model_name:
        :param model_version:
        :return:
        """
        return await self.client.pull_model(model_name, model_version)

    async def delete_model(self, model_name: str, model_version: str):
        """
        Initiate model deletion by ollama engine
        :param model_name:
        :param model_version:
        :return:
        """
        return await self.client.delete_model(model_name, model_version)

    async def generate(self, session_id: str, prompt: str) -> str:
        """
        Prompt the model with user input.
        :param session_id:
        :param prompt:
        :return:
        """

        # Check if session rate limit exceeded
        (
            validation_failed, description
        ) = prompt_validator.check_rate_limit(session_id)

        if validation_failed:
            raise HTTPException(
                status_code=HTTPStatus.TOO_MANY_REQUESTS,
                detail="Rate limit exceeded: {}".format(description)
            )

        # Check prompt for maliciousness before sending it to the model
        (
            validation_failed, description
        ) = prompt_validator.validate_prompt(prompt)

        if validation_failed:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Prompt validation error: {}".format(description)
            )

        return await self.client.generate(session_id, prompt)
