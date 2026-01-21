from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


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
