from datetime import datetime, timedelta
from re import search, IGNORECASE
from typing import Dict, Tuple, Optional
from collections import defaultdict

from src.constants import (
    MAX_REQUESTS_PER_DAY, MAX_REQUESTS_PER_HOUR, MAX_REQUESTS_PER_MINUTE
)
from src.core.services.patterns import all_patterns


class PromptValidatorService:
    """
    This class is used to validate the prompt
    vs different types of maliciousness
    """

    def __init__(self):
        # Rate limiting: session_id -> list of timestamps
        # TODO: move to Redis
        self._requests_history: Dict[str, list] = defaultdict(list)

    def check_rate_limit(self, session_id: str) -> Tuple[bool, Optional[str]]:
        """
        Check if session has exceeded rate limits
        (per minute, per hour, per day).

        Returns:
            Tuple of (exceeded, error_message)
        """

        # Get history for this session
        history = self._requests_history[session_id]

        # Clean old entries
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)

        # Clear history from old entries
        self._requests_history[session_id] = [
            t for t in history if t > day_ago
        ]

        # Count requests for last day
        requests_last_day = len(self._requests_history[session_id])
        if requests_last_day >= MAX_REQUESTS_PER_DAY:
            return (
                True,
                "Too many requests per day ({} allowed)".format(
                    MAX_REQUESTS_PER_DAY
                    )
            )

        requests_last_hour = sum(
            1 for t in history if t > hour_ago
        )
        if requests_last_hour >= MAX_REQUESTS_PER_HOUR:
            return (
                True,
                "Too many requests per hour ({} allowed)".format(
                    MAX_REQUESTS_PER_HOUR
                )
            )

        requests_last_minute = sum(
            1 for t in history if t > minute_ago
        )
        if requests_last_minute >= MAX_REQUESTS_PER_MINUTE:
            return (
                True,
                "Too many requests per minite ({} allowed)".format(
                    MAX_REQUESTS_PER_MINUTE
                )
            )

        # Record this request
        self._requests_history[session_id].append(now)
        return False, None

    def validate_prompt(self, prompt: str) -> (bool, str):
        """
        Validates the prompt vs known malicious patterns
        :param prompt:
        :return:
        """

        for patterns_collection in all_patterns:
            for pattern in patterns_collection.get("patterns"):
                if search(pattern, prompt.lower(), flags=IGNORECASE):
                    return (
                        True,
                        patterns_collection.get("description")
                    )

        return False, ""  # No malicious patterns found in the prompt


prompt_validator = PromptValidatorService()
