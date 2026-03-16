from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette import status

from src.constants import HTTPMethod


async def health_check():
    """
    Service availability endpoint.
    """
    return {"status": "healthy"}


async def index():
    """
    Index page endpoint.
    """
    return FileResponse(
        "static/templates/index.html",
        media_type="text/html"
    )

standard_router = APIRouter()

standard_router.add_api_route(
    "/health",
    endpoint=health_check,
    methods=[HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    summary="Service availability endpoint"
)
standard_router.add_api_route(
    "/",
    endpoint=index,
    methods=[HTTPMethod.GET],
    status_code=status.HTTP_200_OK,
    summary="Index page endpoint"
)
