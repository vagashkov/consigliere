from re import search, IGNORECASE
from src.core.services.patterns import all_patterns


class PromptValidatorService:
    """
    This class is used to validate the prompt
    vs different types of maliciousness
    """

    async def validate_prompt(self, prompt: str) -> bool:
        """
        Validates the prompt vs known malicious patterns
        :param prompt:
        :return:
        """

        for patterns_collection in all_patterns:
            for pattern in patterns_collection.get("patterns"):
                if search(pattern, prompt.lower(), flags=IGNORECASE):
                    return True

        return False
