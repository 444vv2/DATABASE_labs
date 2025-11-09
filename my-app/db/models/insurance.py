from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    Index,
)
from db.base import Base

class Insurance(Base):
    __tablename__ = "insurance"

    insurance_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    country_travel: Mapped[str] = mapped_column(String(45), nullable=False)
    starting_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    finish_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    number_tourist: Mapped[int] = mapped_column(Integer, nullable=False)
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "order.order_id",
            name="fk_insurance_order1"
        ),
        nullable=False
    )
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        Index("fk_insurance_order1_idx", "order_id"),
    )

    order = relationship("Order", back_populates="insurance")
