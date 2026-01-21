from pydantic import BaseModel


class OllamaModelDetails(BaseModel):
    """
    Single LLM details as returned by /api/tags ollama endpoint
    """
    format: str
    parameter_size: str
    quantization_level: str


class OllamaModelData(BaseModel):
    """
    Single LLM data (incl. details) as returned by /api/tags ollama endpoint
    """
    name: str
    size: int
    details: OllamaModelDetails
