from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
)
from db.base import Base

class Event(Base):
    __tablename__ = "event"

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("location.location_id", name="fk_event_location_id"),
        nullable=False,
        index=True
    )
    seat_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=1000)

    location = relationship("Location", back_populates="events")
    artists = relationship("ArtistHasEvent", back_populates="event")
    tickets = relationship("Ticket", back_populates="event")
