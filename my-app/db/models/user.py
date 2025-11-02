from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Integer,
    Index,
)
from db.base import Base

class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(45), nullable=False)
    surname: Mapped[str] = mapped_column(String(45), nullable=False)
    phone: Mapped[str] = mapped_column(String(45), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    __table_args__ = (
        Index('index_email', 'email'),
    )

    orders = relationship("Order", back_populates="user")
    password = relationship("UserPassword", back_populates="user")
