from fastapi import APIRouter

from app.api.endpoints import auth, packages, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(packages.router, prefix="/packages", tags=["packages"])
