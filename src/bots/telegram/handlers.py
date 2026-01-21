from datetime import datetime

from aiogram import Router
from aiogram.filters import (
    Command
)
from aiogram.types import Message

from src.constants import ChatRole
from src.bots.telegram.constants import HELP_TEXT
from src.core.models import ChatMessageDTO
from src.core.services.llm import LLMService
from src.data.storage.dialogs.base import Storage
from src.dependencies import get_active_data_storage
from src.utils import report_error

# Create router for user messages
router = Router()


@router.message(Command("help"))
async def help_command_handler(
        message: Message
) -> None:
    """
    Short and friendly user help manual
    :param message:
    :return:
    """
    await message.answer(
        HELP_TEXT
    )


@router.message()
async def answer(message: Message):
    """
    Answer user's message with LLM response
    :param message:
    :return:
    """

    storage: Storage = get_active_data_storage()

    # Create ChatMessageDTO object
    try:
        user_message = ChatMessageDTO(
            session_id=str(message.chat.id),
            role=ChatRole.USER,
            timestamp=datetime.now().timestamp(),
            content=message.text
        )
        await storage.save_message(user_message)
    except Exception as e:
        report_error(str(e))

    # Forward request to LLM
    response_text = await LLMService().generate(
        str(message.chat.id),
        message.text,
    )

    try:
        system_message = ChatMessageDTO(
            session_id=str(message.chat.id),
            role=ChatRole.SYSTEM,
            timestamp=datetime.now().timestamp(),
            content=response_text
        )
        await storage.save_message(system_message)
    except Exception as e:
        report_error(str(e))

    await message.answer(response_text)
