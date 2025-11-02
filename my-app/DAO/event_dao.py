from typing import  Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Event

class EventDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_event_by_title(self, title: str) -> Optional[Event]:
        query = await self.session.execute(select(Event).where(Event.title == title))
        return query.scalar_one_or_none()

    async def get_event_by_location(self, location: str) -> Optional[Event]:
        query = await self.session.execute(select(Event).where(Event.location == location))
        return query.scalar_one_or_none()

    async def get_event_with_artists(self, event_id: int) -> Optional[Event]:
        query = await self.session.execute(
            select(Event).where(Event.event_id == event_id).options(selectinload(Event.artists))
        )
        return query.scalar_one_or_none()
