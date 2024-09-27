from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import SQLBase
from src.core.database.mixin import TimestampMixin, UUIDMixin


class User(SQLBase, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True, default=None)
    password: Mapped[str] = mapped_column(default=None)
    gauth: Mapped[str] = mapped_column(default=None)
