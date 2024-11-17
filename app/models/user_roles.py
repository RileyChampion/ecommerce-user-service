from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime
from app.db.session import Base
from datetime import datetime


class UserRole(Base):
    __tablename__ = "user_roles"

    role_id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        default=datetime.now(datetime.UTC)
    )
    updated_at: Mapped[DateTime] = mapped_column(
        default=datetime.now(datetime.UTC)
    )

    users = relationship("UserRoleAssignment", back_populates="role")
