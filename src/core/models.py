from pydantic import BaseModel
from typing import List


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
