from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from app.db.session import Base
from datetime import datetime


class UserRoleAssignment(Base):
    __tablename__ = "user_role_assignments"

    assignment_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    role_id: Mapped[int] = mapped_column(ForeignKey('user_roles.role_id'))
    created_at: Mapped[DateTime] = mapped_column(
        default=datetime.now(datetime.UTC)
    )
    updated_at: Mapped[DateTime] = mapped_column(
        default=datetime.now(datetime.UTC)
    )

    user = relationship("User", back_populates="roles")
    role = relationship("UserRole", back_populates="users")
