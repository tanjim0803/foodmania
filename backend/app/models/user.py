from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.models.base import Base
from app.models.mixins import UUIDPrimaryKeyMixin, TimestampMixin


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    image: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(String(15), nullable=False)
