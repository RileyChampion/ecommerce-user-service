from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base
from datetime import datetime


class UserPreference(Base):
    __tablename__ = "user_preferences"

    preference_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    preference_type: Mapped[str] = mapped_column(nullable=False)
    preference_value: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now()
    )

    user = relationship("User", back_populates="preferences")
