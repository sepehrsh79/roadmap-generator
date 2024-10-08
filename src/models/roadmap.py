from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base import SQLBase
from src.core.database.mixin import TimestampMixin, IdMixin

from src.enums import StatusEnum
from src.models import User


class Roadmap(SQLBase, IdMixin, TimestampMixin):
    __tablename__ = "roadmaps"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user: Mapped["User"] = relationship("User", back_populates="roadmaps")
    topic: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)
    status: Mapped[StatusEnum] = mapped_column(default=StatusEnum.learning)
    learning_days: Mapped[list["LearningDay"]] = relationship(back_populates="roadmap")


class LearningDay(SQLBase, IdMixin, TimestampMixin):
    __tablename__ = "learning_days"

    roadmap_id: Mapped[int] = mapped_column(
        ForeignKey("roadmaps.id", ondelete="CASCADE"),
        nullable=False,
    )
    roadmap: Mapped["Roadmap"] = relationship("Roadmap", back_populates="learning_days")
    title: Mapped[str]
    checked: Mapped[bool] = mapped_column(default=False)
    course_link: Mapped[str | None]
    learning_methods: Mapped[str | None]
    online_groups_and_forums: Mapped[str | None]
    time_planning: Mapped[str | None]
    course: Mapped[str | None]
    course_level: Mapped[str | None]
    course_teacher: Mapped[str | None]
    course_type: Mapped[str | None]
    fee: Mapped[str | None]
    has_certificate: Mapped[str | None]