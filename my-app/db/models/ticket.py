from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer,
    ForeignKey,
    DECIMAL,
    Enum,
    Boolean,
    Index
)

from db.base import Base

class Ticket(Base):
    __tablename__ = "ticket"

    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)

    ticket_type: Mapped[str] = mapped_column(
        Enum("bus", "train", "plane", "event", name="ticket_type"),
        nullable=False
    )
    seat_number: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(8, 2), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    bus_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("bus.bus_id", name="fk_ticket_bus1"),
        nullable=True,
        default=None
    )
    train_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("train.train_id", name="fk_ticket_train1"),
        nullable=True,
        default=None
    )
    plane_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("plane.plane_id", name="fk_ticket_plane1"),
        nullable=True,
        default=None
    )
    event_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("event.event_id", name="fk_ticket_event1"),
        nullable=True,
        default=None
    )

    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("order.order_id", name="ticket_ibfk_1"),
        nullable=False
    )

    __table_args__ = (
        Index("idx_ticket_type", "ticket_type"),
        Index("idx_order_id", "order_id"),
        Index("fk_ticket_bus1_idx", "bus_id"),
        Index("fk_ticket_train1_idx", "train_id"),
        Index("fk_ticket_plane1_idx", "plane_id"),
        Index("fk_ticket_event1_idx", "event_id"),
    )

    bus = relationship("Bus", back_populates="tickets")
    train = relationship("Train", back_populates="tickets")
    plane = relationship("Plane", back_populates="tickets")
    event = relationship("Event", back_populates="tickets")
    order = relationship("Order", back_populates="tickets")
