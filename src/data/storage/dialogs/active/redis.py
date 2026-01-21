from datetime import datetime
import json
from redis.commands.json.path import Path as RedisPath
from typing import List

from src.api.v1 import main
from src.data.storage.dialogs.base import ActiveStorage, PersistentStorage
from src.config import get_settings
from src.constants import SESSION_LENGTH
from src.core.models import ChatMessageDTO

settings = get_settings()


class RedisStorage(ActiveStorage):
    """
    Memory-based session storage
    """

    async def get_sessions_list(self) -> List[str]:
        """
        Get all session IDs
        """

        return [
            key for key in main.app.state.redis.keys()
        ]

    async def save_message(self, message: ChatMessageDTO) -> bool:
        """
        Save single message into memory storage
        :param message:
        """
        # First check if it is a first session message
        session_data = main.app.state.redis.json().get(message.session_id)

        if session_data:
            main.app.state.redis.json().arrappend(
                message.session_id,
                RedisPath.root_path(),
                message.model_dump_json()
            )
        else:
            main.app.state.redis.json().set(
                message.session_id,
                RedisPath.root_path(),
                [
                    message.model_dump_json()
                ]
            )

        return True

    async def load_session(self, session_id: str) -> int:
        """
        Load session with designated ID from a persistent storage
        and uploads it into cache for further use
        :param session_id:
        :return:
        """

        # Get messages from persistent storage
        messages = (
            await main.app.state.persistent_storage.load_session(session_id)
        )

        for message in messages:
            await self.save_message(message)

        return len(messages)

    async def get_messages(
            self,
            session_id: str,
            limit: int = SESSION_LENGTH
    ) -> List[ChatMessageDTO]:
        """
        Get messages for a session with specified id
        """
        session_data = main.app.state.redis.json().get(session_id)
        if not session_data:
            return []

        message_strings = (
                              main.app.state.redis.json().get(session_id)
                          )[-limit:]
        messages = [
            json.loads(message) for message in message_strings
        ]
        # Convert to Message objects
        return [
            ChatMessageDTO(
                session_id=message.get("session_id"),
                role=message.get("role"),
                content=message.get("content"),
                timestamp=datetime.fromisoformat(
                    message.get("timestamp")
                )
            )
            for message
            in messages
        ]

    async def delete_session(self, session_id: str) -> bool:
        """
        Delete all messages for a session
        """
        main.app.state.redis.json().delete(
            session_id,
            RedisPath.root_path()
        )

        return True

    async def save_session(
            self,
            session_id: str,
            persistent_storage: PersistentStorage
    ) -> bool:
        """
        Save messages from current session
        :param session_id:
        :param persistent_storage:
        :return:
        """
        if not persistent_storage:
            return False

        if not session_id:
            return False

        messages = await self.get_messages(session_id)

        if messages:
            await persistent_storage.save_session(
                session_id,
                messages
                )

        return True

    async def save_all_sessions(
            self,
            persistent_storage: PersistentStorage
    ) -> bool:
        """
        Save all sessions to persistent storage
        :return:
        """
        if not persistent_storage:
            return False

        sessions_list = await self.get_sessions_list()

        for session_id in sessions_list:
            await self.save_session(
                session_id,
                persistent_storage
            )

        return True
