from pydantic import BaseModel
from typing import Optional

from src.constants import ChatRole
from src.data.llm.openai.constants import FinishReason


class Message(BaseModel):
    """
    Single message validation class
    """

    role: ChatRole
    content: str
    refusal: Optional[str] = None
    annotations: Optional[list] = None


class Choice(BaseModel):
    """
    Alternative response option
    """

    index: int
    message: Message
    finish_reason: FinishReason


class Usage(BaseModel):
    """
    Current request tokens usage data
    """
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class OpenAIAPIResponse(BaseModel):
    """
    OpenAI API response object schema
    """

    id: str
    object: str
    created: int
    model: str
    choices: list[Choice]
    usage: Usage
    system_fingerprint: Optional[str] = None
