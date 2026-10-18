from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(255))
    repo: Mapped[str | None] = mapped_column(String(255), nullable=True)  # owner/name
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
