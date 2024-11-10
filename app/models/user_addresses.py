from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.db.session import Base

class UserAddress(Base):
    __tablename__ = 'user_addresses'

    address_id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    address_line1:Mapped[str] = mapped_column(nullable=True)
    address_line2:Mapped[str] = mapped_column(nullable=True)
    city:Mapped[str] = mapped_column(nullable=True)
    state:Mapped[str] = mapped_column(nullable=True)
    zip_code:Mapped[int] = mapped_column(nullable=True)
    country_code:Mapped[int] = mapped_column(nullable=True)
    is_primary:Mapped[bool] = mapped_column(nullable=False, default=False)

    user:Mapped["User"] = relationship(back_populates="addresses")