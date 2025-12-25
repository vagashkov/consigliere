from datetime import datetime
from json import load, dump
from os import listdir, makedirs, remove
from pathlib import Path
from typing import List, Any

from src.core.models import ChatMessageDTO
from src.data.storage.dialogs.base import PersistentStorage
from src.utils import report_error


class JSONStorage(PersistentStorage):
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

    def __str__(self) -> str:
        return "JSON based storage with path: {}".format(self.storage_path)

    async def get_sessions_list(self) -> List[str]:
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

    async def _get_session_file(self, session_id: str) -> Path:
        """
        Get file path for session chat messages
        :param session_id:
        :return:
        """
        return self.storage_path / "{}.json".format(session_id)

    async def load_session(
            self,
            session_id: str,
            limit: int = 50
    ) -> List[ChatMessageDTO]:
        """
        Get messages for a session with specified id
        """
        file_path = await self._get_session_file(session_id)

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

    async def save_session(
            self,
            session_id: Any,
            messages: List[ChatMessageDTO]
    ) -> bool:
        """
        Save messages history into session-related JSON file
        :param session_id:
        :param messages:
        :return:
        """

        if not messages:
            return False

        if not isinstance(session_id, str):
            session_id = session_id.decode("utf-8")

        file_path = await self._get_session_file(session_id)

        # Write messages into JSON file
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                dump(messages, f, ensure_ascii=False, indent=2, default=str)
        except OSError as e:
            report_error(str(e))

        return True

    async def delete_session(self, session_id: str) -> bool:
        """
        Delete all messages for a session = delete specified file
        """
        file_path = await self._get_session_file(session_id)
        if file_path.exists():
            remove(file_path)

        return True
