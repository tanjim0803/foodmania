from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate


class UserServices:
    async def get_user_by_id(self, db: AsyncSession, id: str):
        stmt = await db.execute(select(User).where(User.id == id))
        user = stmt.scalar_one_or_none()

        if user is None:
            return None

        return True

    async def get_user_by_email(self, db: AsyncSession, email: str):
        stmt = await db.execute(select(User).where(User.email == email))
        user = stmt.scalar_one_or_none()

        if user is None:
            return None

        return True

    async def create_user(self, db: AsyncSession, user_data: UserCreate):
        user = await self.get_user_by_email(db, user_data.email)

        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists!"
            )

        new_user = User(**user_data.model_dump())

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return {"user": new_user}


user_services = UserServices()
