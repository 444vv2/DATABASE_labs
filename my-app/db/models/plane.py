from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer,
    DateTime,
    Index,
    ForeignKey,
    String,
)
from db.base import Base

class Plane(Base):
    __tablename__ = "plane"

    plane_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    plane_class: Mapped[str] = mapped_column("class", String(50), nullable=True, default=None)
    departure_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    arrival_time: Mapped[datetime] = mapped_column(DateTime, nullable=True , default=None)
    from_id: Mapped[int] = mapped_column(Integer,
                                        ForeignKey("location.location_id", name="fk_bus_from"),
                                        nullable=False)
    to_id: Mapped[int] = mapped_column(Integer,
                                       ForeignKey("location.location_id", name="fk_bus_to"),
                                       nullable=False)
    seat_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=150)

    __table_args__ = (
        Index('index_from_id', 'from_id'),
        Index('index_to_id', 'to_id'),
        Index('class_index', 'class', mysql_prefix='FULLTEXT'),
    )
    from_location = relationship("Location", foreign_keys=[from_id], back_populates="planes_from")
    to_location = relationship("Location", foreign_keys=[to_id], back_populates="planes_to")

    tickets = relationship("Ticket", back_populates="plane")
