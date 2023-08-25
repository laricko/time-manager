from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, String, Text, func, text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from security import check_user_admin


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    def as_dict(self) -> dict:
        result = self.__dict__
        result.pop("_sa_instance_state")
        return result


class User(Base):
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(String(31), unique=True)
    password: Mapped[str] = mapped_column(String(127))

    def __repr__(self) -> str:
        return f"User id-{self.id} {self.username}"

    is_anonymous = False
    is_authenticated = True

    def as_dict(self) -> dict:
        r = super().as_dict()
        r.pop("password")
        return r

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, incomed_password) -> bool:
        return check_password_hash(self.password, incomed_password) or check_user_admin(
            self, incomed_password
        )


class Task(Base):
    __tablename__ = "task"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(63))
    description: Mapped[str | None] = mapped_column(Text)
    start: Mapped[datetime]
    finish: Mapped[datetime]

    def as_dict(self):
        r = super().as_dict()
        r["duration"] = str(self.duration)
        r["start"] = str(self.start)[:-3]
        r["finish"] = str(self.finish)[:-3]
        return r

    @hybrid_property
    def duration(self):
        return self.finish - self.start

    __table_args__ = (
        CheckConstraint(text("start < finish"), "check_finish_bigger_than_start"),
    )
