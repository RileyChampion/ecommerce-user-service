from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime
from app.db.session import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    telephone: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    profile_pic: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[DateTime] = mapped_column(
        default=datetime.now(datetime.UTC)
    )
    updated_at: Mapped[DateTime] = mapped_column(
        default=datetime.now(datetime.UTC)
    )

    addresses = relationship("UserAddress", back_populates="user")
    roles = relationship("UserRoleAssignment", back_populates="user")
    preferences = relationship("UserPreference", back_populates="user")
