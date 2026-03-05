from aiogram.types import Update

from fastapi import APIRouter
from fastapi.requests import Request
from starlette import status

from src.bots.telegram.main import bot, dp
from src.constants import HTTPMethod


async def telegram_webhook(request: Request) -> None:
    update = Update.model_validate(
        await request.json(),
        context={"bot": bot}
    )
    await dp.feed_update(bot, update)

router = APIRouter()

router.add_api_route(
    "/telegram",
    endpoint=telegram_webhook,
    methods=[HTTPMethod.POST],
    status_code=status.HTTP_200_OK,
    summary="Webhook endpoint"
)
