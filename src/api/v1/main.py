from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from redis import Redis

from src.api.v1.routes.admin import router as admin_router
from src.api.v1.routes.chat import router as chat_router
from src.api.v1.routes.standard import router as standard_router
from src.api.v1.routes.webhooks import router as webhooks_router
from src.bots.telegram.main import bot, dp
from src.config import get_settings
from src.constants import ActiveStorageType
from src.data.storage.database.postgres import init_db
from src.data.storage.dialogs.base import ActiveStorage, PersistentStorage
import src.dependencies as dependencies

settings = get_settings()
memory_storage: ActiveStorage = dependencies.get_active_data_storage()  # noqa: E501
persistent_storage: PersistentStorage = dependencies.get_persistent_data_storage()  # noqa: E501


# Use webhook mode for Telegram bot
@asynccontextmanager
async def lifespan(application: FastAPI):
    """
    Application lifespan management routine:
    On app startup:
    - enables Telegram bot
    On app shutdown:
    - disables Telegram bot
    :param application:
    :return:
    """

    await bot.set_webhook(
        url=settings.TELEGRAM_WEBHOOK_URL,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    yield
    await bot.delete_webhook()
    await memory_storage.save_all_sessions(persistent_storage)

app_config = {
    "title": settings.APP_TITLE,
    "lifespan": lifespan,
}
if settings.ENVIRONMENT.is_deployed:
    app_config["openapi_url"] = None

app = FastAPI(**app_config)


@app.on_event("startup")
async def on_startup():
    await init_db()

if settings.ACTIVE_STORAGE_TYPE == ActiveStorageType.REDIS:
    app.state.redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "{}/static".format(settings.BASE_URL),
    StaticFiles(directory=settings.STATIC_PATH),
    name="static"
)

app.include_router(
    admin_router,
    prefix="{}/api/v1/admin".format(settings.BASE_URL)
)
app.include_router(
    chat_router,
    prefix="{}/api/v1/chat".format(settings.BASE_URL)
)
app.include_router(
    webhooks_router,
    prefix="{}/api/v1/webhooks".format(settings.BASE_URL)
)
app.include_router(
    standard_router,
    prefix="{}".format(settings.BASE_URL)
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    HTTP exceptions handler
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
        ):
    """
    Request validation error handler
    :param request:
    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=exc.errors()
    )
