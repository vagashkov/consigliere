from datetime import datetime
from pydantic import BaseModel
from typing import List


class LLModelDetails(BaseModel):
    """
    Single LLM details as returned by /api/tags ollama endpoint
    """
    parent_model: str
    format: str
    family: str
    families: List[str]
    parameter_size: str
    quantization_level: str


class LLModelData(BaseModel):
    """
    Single LLM data (incl. details) as returned by /api/tags ollama endpoint
    """
    name: str
    model: str
    modified_at: datetime
    digest: str
    size: int
    details: LLModelDetails


class LLModelsList(BaseModel):
    """
    LLM data list as returned by /api/tags ollama endpoint
    """
    models: List[LLModelData]
