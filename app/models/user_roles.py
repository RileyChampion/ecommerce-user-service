from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class UserRole(Base):
    __tablename__ = "user_roles"

    role_id:Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(nullable=False)

    users = relationship("UserRoleAssignment", back_populates="role")