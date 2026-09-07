from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    name: str
    email: EmailStr
    image: str
