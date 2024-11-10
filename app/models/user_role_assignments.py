from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.db.session import Base

class UserRoleAssignment(Base):
    __tablename__ = "user_role_assignments"

    assignment_id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    role_id:Mapped[int] = mapped_column(ForeignKey('user_roles.role_id'))

    user = relationship("User", back_populates="roles")
    role = relationship("UserRole", back_populates="users")