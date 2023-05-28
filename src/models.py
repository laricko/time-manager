from typing import Optional
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, func
from werkzeug.security import check_password_hash, generate_password_hash


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class User(Base):
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(String(31), unique=True)
    password: Mapped[str] = mapped_column(String(31))

    def __repr__(self) -> str:
        return f"User id-{self.id} {self.username}"

    is_anonymous = False
    is_authenticated = True

    def set_password(self, password):
        """Store the password as a hash for security."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
