from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer,
    DateTime,
    Index,
    ForeignKey,
    Enum,
    Boolean
)
from db.base import Base

class Delivery(Base):
    __tablename__ = "delivery"

    delivery_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    delivery_type: Mapped[str] = mapped_column(
        Enum("courier", "self_pickup", "post_delivery", "email", name="delivery_type"),
        nullable=False
    )
    delivery_time: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
    is_delivered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "order.order_id",
            name="fk_delivery_order1"
        ),
        nullable=False
    )

    __table_args__ = (
        Index('fk_delivery_order1_idx', 'order_id'),
    )

    order = relationship("Order", back_populates="delivery")
