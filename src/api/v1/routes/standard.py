from fastapi import APIRouter
from fastapi.responses import FileResponse

from src.constants import HTTPMethod

from src.config import settings


async def health_check():
    """
    Service availability endpoint.
    """
    return {"status": "healthy"}


async def index():
    """
    Index page endpoint.
    """
    print(settings.STATIC_PATH)
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
    "/",
    endpoint=index,
    methods=[HTTPMethod.GET],
    summary="Index page endpoint"
)
