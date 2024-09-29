from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base import SQLBase
from src.core.database.mixin import TimestampMixin, IdMixin

from src.enums import StatusEnum


class Roadmap(SQLBase, IdMixin, TimestampMixin):
    __tablename__ = "roadmaps"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user: Mapped["User"] = relationship("User", back_populates="roadmaps")
    topic: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)
    status: Mapped[StatusEnum] = mapped_column(default=StatusEnum.learning)


class LearningDay(SQLBase, IdMixin, TimestampMixin):
    __tablename__ = "learning_days"

    roadmap_id: Mapped[int] = mapped_column(
        ForeignKey("roadmaps.id", ondelete="CASCADE"),
        nullable=False,
    )
    roadmap: Mapped["Roadmap"] = relationship("Roadmap", back_populates="learning_days")
    title: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)
    checked: Mapped[bool]
    course_link: Mapped[str | None]
