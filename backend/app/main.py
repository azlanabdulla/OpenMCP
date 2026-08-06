from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
import app.db.base  # Ensure all models are loaded for SQLAlchemy relationships

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="The Open Marketplace for AI Tools API",
    version="0.1.0",
)

# Configure CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME} API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
