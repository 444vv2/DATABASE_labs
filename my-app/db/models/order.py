from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Index,
    Integer,
    DateTime,
    ForeignKey,
    Enum,
)
from db.base import Base

class Order(Base):
    __tablename__ = "order"

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    order_date: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "user.user_id",
            name="fk_order_user",
        ),
        nullable=False
    )
    payment_status: Mapped[str] = mapped_column(
        Enum("pending", "paid", "canceled", name="payment_status"),
        nullable=False,
        default="pending"
    )

    ticket_type: Mapped[str] = mapped_column(
        Enum("bus", "train", "plane", "event", "insurance", name="ticket_type"),
        nullable=False,
    )
    delivery_type: Mapped[str] = mapped_column(
        Enum("email", "courier", "self_pickup", "post_delivery", name="delivery_type"),
        nullable=False,
        default="email"
    )

    __table_args__ = (
        Index('fk_order_user_idx', 'user_id'),
    )

    user = relationship("User", back_populates="orders")

    tickets = relationship("Ticket", back_populates="order")
    delivery = relationship("Delivery", back_populates="order")
    insurance = relationship("Insurance", back_populates="order")
    payment = relationship("Payment", back_populates="order")
