from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Ticket

class TicketDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_available_tickets(self) -> list[Ticket]:
        """Отримання доступних квитків"""
        query = await self.session.execute(select(Ticket).where(Ticket.is_available == True))
        return query.scalars().all()

    async def get_event_tickets(self, event_id: int) -> list[Ticket]:
        """Отримання квитків за ID події"""
        query = await self.session.execute(select(Ticket).where(Ticket.event_id == event_id))
        return query.scalars().all()

    async def get_ticket_by_bus(self, bus_id: int) -> Optional[Ticket]:
        """Отримання квитка за ID автобуса"""
        query = await self.session.execute(select(Ticket).where(Ticket.bus_id == bus_id))
        return query.scalar_one_or_none()

    async def get_ticket_by_train(self, train_id: int) -> Optional[Ticket]:
        """Отримання квитка за ID потяга"""
        query = await self.session.execute(select(Ticket).where(Ticket.train_id == train_id))
        return query.scalar_one_or_none()

    async def get_ticket_by_plane(self, plane_id: int) -> Optional[Ticket]:
        """Отримання квитка за ID літака"""
        query = await self.session.execute(select(Ticket).where(Ticket.plane_id == plane_id))
        return query.scalar_one_or_none()

    async def get_ticket_by_event(self, event_id: int) -> Optional[Ticket]:
        """Отримання квитка за ID події"""
        query = await self.session.execute(select(Ticket).where(Ticket.event_id == event_id))
        return query.scalar_one_or_none()
