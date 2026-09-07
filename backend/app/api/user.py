from fastapi import APIRouter, Form, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database.session import SessionDep
from app.services.user import user_services
from pydantic import EmailStr
from app.models.enums import Roles
from typing import Annotated

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register_user(
    db: SessionDep,
    name: str = Form(..., min_length=3, max_length=50),
    email: EmailStr = Form(...),
    password: str = Form(..., min_length=6, max_length=50),
    image: str = Form(...),
    role: Roles = Form(...),
):
    return await user_services.create_user(db, name, email, password, image, role)


@router.post("/login")
async def login_with_email_password(
    db: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return await user_services.sign_in_with_email_password(
        db, form_data.username, form_data.password
    )


@router.post("/refresh")
async def refresh(db: SessionDep, token: str):
    return await user_services.refresh_token(db, token)
