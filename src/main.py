from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.api.v1.routes.service import router as service_router
from src.api.v1.routes.chat import router as chat_router

app = FastAPI(title="Consigliere API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    service_router,
    prefix="/api/v1/service"
)

app.include_router(
    chat_router,
    prefix="/api/v1/chat"
)


@app.get("/health")
async def health_check():
    """
    Service availability endpoint.
    """
    return {"status": "healthy"}


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
