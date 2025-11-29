from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer,
    DateTime,
    Index,
    ForeignKey,
)
from db.base import Base

class Bus(Base):
    __tablename__ = "bus"

    bus_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    departure_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    arrival_time: Mapped[datetime] = mapped_column(DateTime, nullable=True , default=None)
    from_id: Mapped[int] = mapped_column(Integer,
                                        ForeignKey("location.location_id", name="fk_bus_from"),
                                        nullable=False)
    to_id: Mapped[int] = mapped_column(Integer,
                                       ForeignKey("location.location_id", name="fk_bus_to"),
                                       nullable=False)
    seat_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=50)

    __table_args__ = (
        Index('index_from_id', 'from_id'),
        Index('index_to_id', 'to_id'),
    )

    from_location = relationship("Location", foreign_keys=[from_id], back_populates="buses_from")
    to_location = relationship("Location", foreign_keys=[to_id], back_populates="buses_to")

    tickets = relationship("Ticket", back_populates="bus")
