from aiogram import Router
from aiogram.filters import (
    CommandObject, CommandStart, Command
)
from aiogram.types import Message
from aiogram.utils.formatting import Text

from src.bots.telegram.constants import HELP_TEXT

# Create router for user messages
commands_router = Router()


@commands_router.message(Command("help"))
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


@commands_router.message(CommandStart())
async def command_start_handler(
    message: Message
) -> None:
    """
    /start command handler
    :param message:
    :return:
    """
    # Build reply content in case if user's name contains
    # some 'HTML-like' parts that need to be escaped
    content = Text(
        "Got your message, ",
        message.from_user.full_name
    )
    # Reply using unfolded content
    await message.reply(
        **content.as_kwargs()
    )


@commands_router.message(Command("search"))
async def command_search_handler(
        message: Message,
        command: CommandObject
) -> None:
    """
    /search command handler
    :param message:
    :param command:
    :return:
    """
    # Check if search text exists
    if command.args is None:
        await message.answer(
            "Error: nothing to search"
        )
        return

    # Build reply content in case if user's name contains
    # some 'HTML-like' parts that need to be escaped
    content = Text(
        "Got your message, ",
        message.from_user.full_name
    )
    # Reply using unfolded content
    await message.reply(
        **content.as_kwargs()
    )
