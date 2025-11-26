from src.core.services import (
    LLMService, OllamaLLMService
)


class LLMServiceDependency:
    """
    """
    @staticmethod
    def get_llm_service() -> LLMService:
        """
        Get the LLM service
        :return:
        """
        return OllamaLLMService()
