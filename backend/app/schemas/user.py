from pydantic import BaseModel, EmailStr
from app.models.enums import RoleScope


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    image: str
    role: RoleScope
