from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.session import Base
from datetime import datetime


class UserRole(Base):
    __tablename__ = "user_roles"

    role_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role_name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now()
    )

    users = relationship("UserRoleAssignment", back_populates="role")
