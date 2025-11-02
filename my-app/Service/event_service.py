from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from DAO.event_dao import EventDAO
from DAO.general_dao import GeneralDAO
from db.models import Event
from schemas.event import EventCreate, EventUpdate, EventResponse


class EventService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.event_dao = EventDAO(session)
        self.general_dao = GeneralDAO[Event](session)

    async def create_event(self, event_data: EventCreate) -> EventResponse:
        """Створення події"""
        new_event = Event(
            title=event_data.title,
            date_time=event_data.date_time,
            location_id=event_data.location_id,
            seat_amount=event_data.seat_amount
        )
        created_event = await self.general_dao.create(new_event)
        return EventResponse.model_validate(created_event)

    async def get_event_by_id(self, event_id: int) -> Optional[EventResponse]:
        """Отримання події за ID"""
        event = await self.general_dao.get_by_id(Event, event_id)
        if event:
            return EventResponse.model_validate(event)
        return None

    async def get_all_events(self) -> List[EventResponse]:
        """Отримання всіх подій"""
        events = await self.general_dao.get_all(Event)
        return [EventResponse.model_validate(event) for event in events]

    async def update_event(self, event_id: int, event_data: EventUpdate) -> Optional[EventResponse]:
        """Оновлення події"""
        event = await self.general_dao.get_by_id(Event, event_id)
        if not event:
            return None

        for field, value in event_data.model_dump(exclude_unset=True).items():
            setattr(event, field, value)

        updated_event = await self.general_dao.update(event)
        return EventResponse.model_validate(updated_event)

    async def delete_event(self, event_id: int) -> bool:
        """Видалення події"""
        return await self.general_dao.delete_by_id(Event, event_id)

    async def get_events_by_location(self, location_id: int) -> List[EventResponse]:
        """Отримання подій за локацією"""
        query = await self.session.execute(
            select(Event).where(Event.location_id == location_id)
        )
        events = query.scalars().all()
        return [EventResponse.model_validate(event) for event in events]

    async def get_upcoming_events(self) -> List[EventResponse]:
        """Отримання майбутніх подій"""
        query = await self.session.execute(
            select(Event).where(Event.date_time > datetime.now()).order_by(Event.date_time)
        )
        events = query.scalars().all()
        return [EventResponse.model_validate(event) for event in events]

    async def get_event_by_title(self, title: str) -> Optional[EventResponse]:
        """Пошук події за назвою"""
        event = await self.event_dao.get_event_by_title(title)
        if event:
            return EventResponse.model_validate(event)
        return None
