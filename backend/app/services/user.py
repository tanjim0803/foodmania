from fastapi import HTTPException, status
from app.models.user import User
from app.models.refresh_token import RefreshToken
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.utils.user import (
    password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.config import security_settings
from datetime import datetime, timezone, timedelta
from app.models.enums import Roles


class UserServices:
    async def get_user_by_id(self, db: AsyncSession, id: str):
        stmt = await db.execute(select(User).where(User.id == id))
        user = stmt.scalar_one_or_none()

        if user is None:
            return None

        return user

    async def get_user_by_email(self, db: AsyncSession, email: str):
        stmt = await db.execute(select(User).where(User.email == email))
        user = stmt.scalar_one_or_none()

        if user is None:
            return None

        return user

    async def create_user(
        self,
        db: AsyncSession,
        name: str,
        email: str,
        password: str,
        image: str,
        role: Roles,
    ):
        user_exists = await self.get_user_by_email(db, email)

        if user_exists is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists!"
            )

        new_user = User(
            name=name,
            email=email,
            hashed_password=password_hash(password),
            image=image,
            role=role,
        )

        db.add(new_user)
        await db.commit()
        db.refresh(new_user)

        return {"message": "User successfully created!"}

    async def sign_in_with_email_password(
        self, db: AsyncSession, email: str, password: str
    ):
        user = await self.get_user_by_email(db, email)

        print("User: ", user)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))

        db_refresh_token = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expired_at=datetime.now(tz=timezone.utc)
            + timedelta(days=security_settings.JWT_REFRESH_TOKEN_TIME_DAY),
        )

        db.add(db_refresh_token)
        await db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_token(self, db: AsyncSession, token: str):
        try:
            token_decode = decode_token(token)
            if token_decode.get("type") != "refresh_token":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type!",
                )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token!",
            )

        stmt = await db.execute(select(RefreshToken).where(RefreshToken.token == token))
        token_exists = stmt.scalar_one_or_none()

        if not token_exists or token_exists.revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid or revoked!",
            )

        if token_exists.expired_at < datetime.now(tz=timezone.utc):
            token_exists.revoked = True
            await db.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired. Please log in again!",
            )

        access_token = create_access_token(token_exists.user_id)

        return {"access_token": access_token, "token_type": "bearer"}


user_services = UserServices()
