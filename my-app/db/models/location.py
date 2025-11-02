from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Integer
)
from db.base import Base

class Location(Base):
    __tablename__ = "location"

    location_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)

    events = relationship("Event", back_populates="location")

    buses_from = relationship("Bus", foreign_keys="Bus.from_id", back_populates="from_location")
    buses_to = relationship("Bus", foreign_keys="Bus.to_id", back_populates="to_location")

    trains_from = relationship("Train", foreign_keys="Train.from_id", back_populates="from_location")
    trains_to = relationship("Train", foreign_keys="Train.to_id", back_populates="to_location")

    planes_from = relationship("Plane", foreign_keys="Plane.from_id", back_populates="from_location")
    planes_to = relationship("Plane", foreign_keys="Plane.to_id", back_populates="to_location")
