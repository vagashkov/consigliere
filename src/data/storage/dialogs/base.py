""" Abstract storage interface """

from abc import ABC, abstractmethod
from typing import List

from src.core.models import ChatMessageDTO


class Storage(ABC):
    """Abstract storage interface."""

    @abstractmethod
    async def save_message(
            self,
            message: ChatMessageDTO
    ) -> None:
        """Save single chat message to a storage"""
        pass

    @abstractmethod
    async def get_messages(
            self,
            session_id: str,
            limit: int = 50
    ) -> List[ChatMessageDTO]:
        """Get messages for specified session from a storage"""
        pass

    @abstractmethod
    async def delete_session(
            self,
            session_id: str
    ) -> None:
        """Delete all messages for specified session from a storage"""
        pass

    @abstractmethod
    async def get_all_sessions(self) -> List[str]:
        """Get all existing session IDs from a storage"""
        pass
