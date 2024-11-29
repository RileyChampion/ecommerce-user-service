from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.session import Base
from datetime import datetime
from app.models.user_role_assignments import UserRoleAssignment


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    telephone: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    profile_pic: Mapped[str] = mapped_column(
        nullable=False,
        default="default.png"
    )
    is_active: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now()
    )

    addresses = relationship("UserAddress", back_populates="user", cascade='all, delete')
    roles = relationship(
        "UserRole",
        secondary="user_role_assignments",
        back_populates="assignments"
    )
    preferences = relationship("UserPreference", back_populates="user", cascade='all, delete')
