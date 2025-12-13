from aiogram.types import Update

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import FileResponse

from src.bots.telegram.main import bot, dp
from src.constants import HTTPMethod


async def health_check():
    """
    Service availability endpoint.
    """
    return {"status": "healthy"}


async def webhook(request: Request) -> None:
    update = Update.model_validate(
        await request.json(),
        context={"bot": bot}
    )
    await dp.feed_update(bot, update)


async def index():
    """
    Index page endpoint.
    """
    return FileResponse(
        "static/templates/index.html",
        media_type="text/html"
    )

router = APIRouter()

router.add_api_route(
    "/health",
    endpoint=health_check,
    methods=[HTTPMethod.GET],
    summary="Service availability endpoint"
)
router.add_api_route(
    "/webhook",
    endpoint=webhook,
    methods=[HTTPMethod.POST],
    summary="Webhook endpoint"
)
router.add_api_route(
    "/",
    endpoint=index,
    methods=[HTTPMethod.GET],
    summary="Index page endpoint"
)
