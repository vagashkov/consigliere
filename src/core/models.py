from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime


class LLMProviderRequestDTO(BaseModel):
    """
    Single create LLM provider data transfer object
    """

    name: str = Field(min_length=3, max_length=255)
    url: str = Field(min_length=3, max_length=255)
    port: int = Field(ge=1, le=65535)
    description: str = Field(min_length=3, max_length=255)


class LLMProviderResponseDTO(BaseModel):
    """
    Single LLM provider data transfer object
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    url: str
    port: int
    description: str


class LLModelDTO(BaseModel):
    """
    Single LLM data transfer object
    """
    name: str
    size: int
    format: str
    parameters: str
    quantization_level: str


class LLModelDTOList(BaseModel):
    """
    LLM data transfer objects list
    """
    models: List[LLModelDTO]


class ChatRequestDTO(BaseModel):
    """
    Chat request data transfer object
    """
    session_id: str
    content: str


class ChatResponseDTO(BaseModel):
    """
    Chat response data transfer object
    """
    session_id: str
    content: str


class ChatMessageDTO(BaseModel):
    """
    Single chat message
    """
    session_id: str
    role: str
    content: str
    timestamp: Optional[datetime]
