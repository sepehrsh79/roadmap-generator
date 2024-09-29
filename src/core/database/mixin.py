import datetime
from uuid import uuid4
from sqlalchemy import BigInteger, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now(),
        onupdate=datetime.datetime.now(),
        nullable=False,
    )


class IdMixin:
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
        autoincrement=True,
    )


class UUIDMixin:
    id: Mapped[UUID] = mapped_column(
        UUID,
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid4,
    )
