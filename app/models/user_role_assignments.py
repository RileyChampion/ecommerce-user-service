from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base
from datetime import datetime


class UserRoleAssignment(Base):
    __tablename__ = "user_role_assignments"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('user_roles.role_id', ondelete="CASCADE"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now()
    )

    # user = relationship("User", back_populates="roles")
    # role = relationship("UserRole", back_populates="assignments")
