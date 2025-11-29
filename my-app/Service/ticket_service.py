from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from DAO.ticket_dao import TicketDAO
from DAO.general_dao import GeneralDAO
from db.models import Ticket
from schemas.ticket import TicketCreate, TicketUpdate, TicketResponse


class TicketService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.ticket_dao = TicketDAO(session)
        self.general_dao = GeneralDAO[Ticket](session)

    async def create_ticket(self, ticket_data: TicketCreate) -> TicketResponse:
        """
        Створення квитка
        """
        bus_id = None if ticket_data.bus_id == 0 else ticket_data.bus_id
        plane_id = None if ticket_data.plane_id == 0 else ticket_data.plane_id
        train_id = None if ticket_data.train_id == 0 else ticket_data.train_id
        event_id = None if ticket_data.event_id == 0 else ticket_data.event_id

        new_ticket = Ticket(
            ticket_type=ticket_data.ticket_type,
            seat_number=ticket_data.seat_number,
            price=ticket_data.price,
            is_available=ticket_data.is_available,
            bus_id=bus_id,
            plane_id=plane_id,
            train_id=train_id,
            event_id=event_id,
            order_id=ticket_data.order_id
        )
        created_ticket = await self.general_dao.create(new_ticket)
        return TicketResponse.model_validate(created_ticket)

    async def get_ticket_by_id(self, ticket_id: int) -> Optional[TicketResponse]:
        """
        Отримання квитка за ID
        """
        ticket = await self.general_dao.get_by_id(Ticket, ticket_id)
        if ticket:
            return TicketResponse.model_validate(ticket)
        return None

    async def update_ticket(self, ticket_id: int, ticket_data: TicketUpdate) -> Optional[TicketResponse]:
        """
        Оновлення інформації про квиток
        """
        ticket = await self.general_dao.get_by_id(Ticket, ticket_id)
        if not ticket:
            return None

        for field, value in ticket_data.model_dump(exclude_unset=True).items():
            setattr(ticket, field, value)

        updated_ticket = await self.general_dao.update(ticket)
        return TicketResponse.model_validate(updated_ticket)

    async def delete_ticket(self, ticket_id: int) -> bool:
        """
        Видалення квитка за ID
        """
        result = await self.general_dao.delete_by_id(Ticket, ticket_id)
        return result

    async def get_all_tickets(self) -> List[TicketResponse]:
        """
        Отримання всіх квитків
        """
        tickets = await self.general_dao.get_all(Ticket)
        return [TicketResponse.model_validate(ticket) for ticket in tickets]

    async def get_ticket_by_bus(self, bus_id: int) -> List[TicketResponse]:
        """
        Отримання квитків за ID автобуса
        """
        ticket = await self.ticket_dao.get_ticket_by_bus(bus_id)
        return [TicketResponse.model_validate(ticket)] if ticket else []

    async def get_ticket_by_train(self, train_id: int) -> List[TicketResponse]:
        """
        Отримання квитків за ID поїзда
        """
        ticket = await self.ticket_dao.get_ticket_by_train(train_id)
        return [TicketResponse.model_validate(ticket)] if ticket else []

    async def get_ticket_by_plane(self, plane_id: int) -> List[TicketResponse]:
        """
        Отримання квитків за ID літака
        """
        ticket = await self.ticket_dao.get_ticket_by_plane(plane_id)
        return [TicketResponse.model_validate(ticket)] if ticket else []

    async def get_ticket_by_event(self, event_id: int) -> List[TicketResponse]:
        """
        Отримання квитків за ID події
        """
        tickets = await self.ticket_dao.get_event_tickets(event_id)
        return [TicketResponse.model_validate(ticket) for ticket in tickets]

    async def get_avg_price_for_event(self) -> float:
        try:
            result = await self.session.execute(
                text("CALL calling_func()")
            )
            await self.session.commit()

            row = result.fetchone()
            if row is not None:
                return float(row[0])
            return 0.0
        except Exception as e:
            await self.session.rollback()
            raise e from e
