from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from app.db.session import Base
from datetime import datetime


class UserPreference(Base):
    __tablename__ = "user_preferences"

    preference_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    preference_type: Mapped[str] = mapped_column(nullable=False)
    preference_value: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        default=datetime.now(datetime.UTC)
    )
    updated_at: Mapped[DateTime] = mapped_column(
        default=datetime.now(datetime.UTC)
    )

    user = relationship("User", back_populates="preferences")
