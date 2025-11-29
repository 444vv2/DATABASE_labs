from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    Text,
    Integer,
    Index,
    DATETIME
)
from db.base import Base

class Comment(Base):
    __tablename__ = "comment"

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    descriptions: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DATETIME, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index('index_user_id', 'user_id'),
    )
