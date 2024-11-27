from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base
from datetime import datetime


class UserRoleAssignment(Base):
    __tablename__ = "user_role_assignments"

    assignment_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    role_id: Mapped[int] = mapped_column(ForeignKey('user_roles.role_id'))
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now()
    )

    user = relationship("User", back_populates="roles")
    role = relationship("UserRole", back_populates="users")
