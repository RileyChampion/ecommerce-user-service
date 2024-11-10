from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.db.session import Base

class UserPreference(Base):
    __tablename__ = "user_preferences"

    preference_id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    preference_type:Mapped[str] = mapped_column(nullable=False)
    preference_value:Mapped[str] = mapped_column(nullable=False)

    user = relationship("User", back_populates="preferences")

