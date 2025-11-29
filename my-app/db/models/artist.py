from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Index,
    UniqueConstraint
)

from db.base import Base

class Artist(Base):
    __tablename__ = "artist"

    artist_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    nickname: Mapped[str] = mapped_column(String(50), nullable=True, default=None)
    genre: Mapped[str] = mapped_column(String(50), nullable=True, default=None)
    is_group: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)

    __table_args__ = (
        UniqueConstraint('name', 'surname', name='unique_name_surname'),
        Index('index_surname', 'surname', mysql_prefix='FULLTEXT'),
    )

    events = relationship("ArtistHasEvent", back_populates="artist")
