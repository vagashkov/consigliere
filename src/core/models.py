from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime


class UserRequestDTO(BaseModel):
    """
    User create/update data transfer object
    """

    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=3, max_length=32)
    role: str = Field(min_length=3, max_length=32)


class AccessToken(BaseModel):
    """
    Access token (JWT etc)
    """
    token_type: str
    token_value: str


class UserResponseDTO(BaseModel):
    """
    User get data transfer object
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    is_active: bool
    role: str


class LoginRequestDTO(BaseModel):
    """
    User login data transfer object
    """

    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=3, max_length=32)


class LoginResponseDTO(BaseModel):
    """
    User login data transfer object
    """

    pass


class LLMProviderRequestDTO(BaseModel):
    """
    Single LLM provider create/update data transfer object
    """

    name: str = Field(min_length=3, max_length=255)
    url: str = Field(min_length=3, max_length=255)
    port: int = Field(ge=1, le=65535)
    description: str = Field(min_length=3, max_length=255)


class LLMProviderResponseDTO(BaseModel):
    """
    Single LLM provider get data transfer object
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    url: str
    port: int
    description: str


class LLMRequestDTO(BaseModel):
    """
    Single LLM create/update data transfer object
    """

    name: str
    size: int
    format: str
    parameters: str
    quantization_level: str


class LLModelDTO(BaseModel):
    """
    ToDo: LEGACY CLASS TO BE REFACTORED
    Single LLM create/update data transfer object
    """

    name: str
    size: int
    format: str
    parameters: str
    quantization_level: str


class LLMResponseDTO(BaseModel):
    """
    Single LLM get data transfer object
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
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
