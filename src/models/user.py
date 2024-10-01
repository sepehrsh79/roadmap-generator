from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database.base import SQLBase
from src.core.database.mixin import TimestampMixin, UUIDMixin


class User(SQLBase, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True, default=None, index=True)
    password: Mapped[str] = mapped_column(default=None)
    gauth: Mapped[str] = mapped_column(default=None)
    email: Mapped[str | None] = mapped_column(unique=True, default=None, index=True)
    inputs: Mapped[list["Input"]] = relationship(back_populates="user")
    roadmaps: Mapped[list["Roadmap"]] = relationship(back_populates="user")
