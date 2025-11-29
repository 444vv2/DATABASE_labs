from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer,
    Index,
    ForeignKey,
)
from db.base import Base

class ArtistHasEvent(Base):
    __tablename__ = "artist_has_event"

    artist_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("artist.artist_id", name="fk_artist_has_event_artist1"),
        primary_key=True
    )
    event_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("event.event_id", name="fk_artist_has_event_event1"),
        primary_key=True
    )

    __table_args__ = (
        Index("fk_artist_has_event_artist1_idx", "artist_id"),
        Index("fk_artist_has_event_event1_idx", "event_id"),
    )

    artist = relationship("Artist", back_populates="events")
    event = relationship("Event", back_populates="artists")
