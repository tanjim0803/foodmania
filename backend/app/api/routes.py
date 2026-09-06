from fastapi import APIRouter
from app.api.user import router as user_router

routers = APIRouter(prefix="/api/v1")

routers.include_router(user_router)
