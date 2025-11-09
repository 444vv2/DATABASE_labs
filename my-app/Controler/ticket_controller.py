from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_db
from Service import TicketService
from schemas.ticket import TicketCreate, TicketUpdate, TicketResponse

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.get("/", response_model=List[TicketResponse])
async def get_all_tickets(db: AsyncSession = Depends(get_db)):
    """Отримати всі квитки"""
    ticket_service = TicketService(db)
    return await ticket_service.get_all_tickets()

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket_by_id(ticket_id: int, db: AsyncSession = Depends(get_db)):
    """Отримати квиток за ID"""
    ticket_service = TicketService(db)
    ticket = await ticket_service.get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with id {ticket_id} not found"
        )
    return ticket

@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket_data: TicketCreate, db: AsyncSession = Depends(get_db)):
    """Створити новий квиток"""
    ticket_service = TicketService(db)
    try:
        return await ticket_service.create_ticket(ticket_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id: int, ticket_data: TicketUpdate, db: AsyncSession = Depends(get_db)):
    """Оновити квиток"""
    ticket_service = TicketService(db)
    try:
        updated_ticket = await ticket_service.update_ticket(ticket_id, ticket_data)
        if not updated_ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket with id {ticket_id} not found"
            )
        return updated_ticket
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    """Видалити квиток"""
    ticket_service = TicketService(db)
    deleted = await ticket_service.delete_ticket(ticket_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with id {ticket_id} not found"
        )
