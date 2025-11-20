from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.app.handlers.service import router as service_router

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


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
