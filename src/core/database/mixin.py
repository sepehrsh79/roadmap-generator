import datetime
from uuid import uuid4
from sqlalchemy import BigInteger, DateTime, func, UUID
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column


class TimestampMixin(MappedAsDataclass):
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now(), nullable=False
    )


class IdMixin(MappedAsDataclass):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)


class UUIDMixin(MappedAsDataclass):
    id: Mapped[UUID] = mapped_column(
        UUID,
        primary_key=True,
        unique=True,
        nullable=False,
        default_factory=uuid4,
    )
