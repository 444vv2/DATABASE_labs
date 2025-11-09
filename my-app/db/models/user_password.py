from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
)
from db.base import Base

class UserPassword(Base):
    __tablename__ = "user_password"

    password_hash: Mapped[str] = mapped_column(String(225), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.user_id", name="fk_user_password_user1"),
        primary_key=True,
        nullable=False
    )

    user = relationship("User", back_populates="password")
