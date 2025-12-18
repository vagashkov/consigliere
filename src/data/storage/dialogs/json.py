from datetime import datetime
from json import load, loads, dump
from os import listdir, makedirs, remove
from pathlib import Path
from typing import List

from src.api.v1 import main
from src.core.models import ChatMessageDTO
from src.data.storage.dialogs.base import Storage
from src.utils import report_error


class JSONStorage(Storage):
    """
    JSON file-based storage
    """

    def __init__(self, data_path: Path):
        """
        Storage initialization:
        - create directory if it doesn't exist
        - save data path location for farther usage
        :param data_path:
        """
        storage_path = Path(data_path) / "dialogs"

        try:
            makedirs(storage_path, exist_ok=True)
        except OSError as e:
            report_error(str(e))
        self.storage_path = storage_path

    def _get_session_file(self, session_id: str) -> Path:
        """
        Get file path for session chat messages
        :param session_id:
        :return:
        """
        return self.storage_path / "{}.json".format(session_id)

    async def save_message(self, message: ChatMessageDTO) -> None:
        """
        Save single message into session-related JSON file
        """
        file_path = self._get_session_file(message.session_id)

        # Load existing messages
        messages = []
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    messages = load(f)
            except OSError as e:
                report_error(str(e))

        # Append new message
        messages.append(message.dict())

        # Load messages back into JSON file
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                dump(messages, f, ensure_ascii=False, indent=2, default=str)
        except OSError as e:
            report_error(str(e))

    async def save_session(self, session_id: str | bytes) -> None:
        """
        Save messages history into session-related JSON file
        :param session_id:
        :return:
        """
        file_name = str(session_id.decode("utf-8"))
        file_path = self._get_session_file(file_name)

        message_strings = main.app.state.redis.json().get(session_id)

        messages = [loads(message) for message in message_strings]

        # Load messages into JSON file
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                dump(messages, f, ensure_ascii=False, indent=2, default=str)
        except OSError as e:
            report_error(str(e))

    async def get_messages(
            self,
            session_id: str,
            limit: int = 50
    ) -> List[ChatMessageDTO]:
        """
        Get messages for a session with specified id
        """
        file_path = self._get_session_file(session_id)

        # No file yet
        if not file_path.exists():
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                all_messages = load(f)
        except OSError as e:
            report_error(str(e))

        # Convert to Message objects
        return [
            ChatMessageDTO(
                session_id=item.get("session_id"),
                role=item.get("role"),
                content=item.get("content"),
                timestamp=datetime.fromisoformat(
                    item.get("timestamp")
                )
            )
            for item
            in all_messages[-limit:]  # Getting last N messages only
        ]

    async def delete_session(self, session_id: str) -> None:
        """
        Delete all messages for a session = delete specified file
        """
        file_path = self._get_session_file(session_id)
        if file_path.exists():
            remove(file_path)

    async def get_all_sessions(self) -> List[str]:
        """
        Get all session IDs
        """

        return [
            # Remove .json
            filename[:-5]
            # From every file id data_path directory
            for filename in listdir(self.storage_path)
            # With .json extension
            if filename.endswith(".json")
        ]
