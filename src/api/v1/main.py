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
import src.dependencies as dependencies

settings = get_settings()
memory_storage = dependencies.get_data_storage()


# Use webhook mode for Telegram bot
@asynccontextmanager
async def lifespan(application: FastAPI):
    await bot.set_webhook(
        url=settings.TELEGRAM_WEBHOOK_URL,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    yield
    await bot.delete_webhook()
    await memory_storage.save_all_sessions()

app = FastAPI(title="Consigliere Web API", lifespan=lifespan)

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

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(admin_router, prefix="/api/v1/admin")
app.include_router(chat_router, prefix="/api/v1/chat")
app.include_router(webhooks_router, prefix="/api/v1/webhooks")
app.include_router(standard_router)


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
