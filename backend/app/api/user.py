from fastapi import APIRouter
from app.database.session import SessionDep
from app.schemas.user import UserCreate
from app.services.user import user_services

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register_user(db: SessionDep, user: UserCreate):
    return await user_services.create_user(db, user)
