""" Abstract storage interface """

from abc import ABC, abstractmethod
from typing import List

from src.core.models import ChatMessageDTO
from src.constants import SESSION_LENGTH


class Storage(ABC):
    """Abstract storage interface."""

    @abstractmethod
    async def get_sessions_list(self) -> List[str]:
        """Get all existing session IDs from a storage"""
        pass

    @abstractmethod
    async def delete_session(
            self,
            session_id: str
    ) -> bool:
        """Delete all messages for specified session from a storage"""
        pass


class PersistentStorage(Storage):
    """
    Persistent storage interface
    """

    @abstractmethod
    async def save_session(
            self,
            session_id: str,
            messages: List[ChatMessageDTO]
    ) -> bool:
        """"
        Save session content with designated ID to a persistent storage
        """
        pass


class ActiveStorage(Storage):
    """
    Active storage interface
    """

    @abstractmethod
    async def load_session(self, session_id: str) -> bool:
        """
        Load session with designated ID from a persistent storage
        :param session_id:
        :return:
        """
        pass

    @abstractmethod
    async def get_messages(
            self, session_id: str, limit: int = SESSION_LENGTH
    ) -> List[ChatMessageDTO]:
        """
        Load session with designated ID from a persistent storage
        :param session_id:
        :param limit:
        :return:
        """
        pass

    @abstractmethod
    async def save_message(
            self,
            message: ChatMessageDTO
    ) -> bool:
        """Save single chat message to a storage"""
        pass

    @abstractmethod
    async def save_all_sessions(
            self,
            persistent_storage: PersistentStorage
    ) -> bool:
        """"
        Save session with designated ID to a persistent storage
        """
        pass

    @abstractmethod
    async def save_session(
            self,
            session_id: str,
            persistent_storage: PersistentStorage
    ) -> bool:
        """"
        Save session with designated ID to a persistent storage
        """
        pass
