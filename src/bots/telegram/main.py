from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.config import get_settings
from src.bots.telegram.handlers import router

config = get_settings()

# Create new bot
bot = Bot(
    token=config.TELEGRAM_TOKEN.get_secret_value(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
        )
    )
# Clear updates history during bot inactivity
if config.DISABLE_PENDING_MESSAGES:
    bot.delete_webhook(drop_pending_updates=True)

# Create dispatcher
memory_storage = MemoryStorage()
dp = Dispatcher(storage=memory_storage)

# Setup dispatcher routes
main_router = Router()
main_router.include_router(router)
dp.include_router(main_router)
