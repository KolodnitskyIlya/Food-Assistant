from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    goal: Mapped[str] = mapped_column(String(50))
    cooking_time: Mapped[int] = mapped_column()  # minutes
    ingredients: Mapped[str] = mapped_column(Text)  # comma-separated string
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user: Mapped["User"] = relationship("User", back_populates="recipes")