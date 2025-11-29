from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer,
    DateTime,
    ForeignKey,
    String,
    DECIMAL,
    Enum,
    Boolean,
    Index
)
from db.base import Base

class Payment(Base):
    __tablename__ = "payment"

    payment_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    amount: Mapped[float] = mapped_column(DECIMAL(8, 2), nullable=False)
    payment_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    payment_type: Mapped[str] = mapped_column(
        Enum("card", "google_pay", "cash", name="payment_type"), nullable=False
    )
    is_paid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    transaction_number: Mapped[str] = mapped_column(String(150), nullable=True, default=None)
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "order.order_id", 
            name="fk_payment_order1",
            ondelete="NO ACTION",
            onupdate="NO ACTION"
        ),
        nullable=False,
        unique=True
    )

    __table_args__ = (
        Index('fk_payment_order1_idx', 'order_id', unique=True),
    )

    order = relationship("Order", back_populates="payment")
