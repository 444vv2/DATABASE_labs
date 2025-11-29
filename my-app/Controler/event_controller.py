from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_db
from Service import EventService, TicketService
from schemas.event import EventCreate, EventUpdate, EventResponse, EventWithArtistsResponse
from schemas.ticket import TicketResponse

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/", response_model=List[EventResponse])
async def get_all_events(db: AsyncSession = Depends(get_db)):
    """Отримати всі події"""
    event_service = EventService(db)
    return await event_service.get_all_events()

@router.get("/{event_id}", response_model=EventResponse)
async def get_event_by_id(event_id: int, db: AsyncSession = Depends(get_db)):
    """Отримати подію за ID"""
    event_service = EventService(db)
    event = await event_service.get_event_by_id(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found"
        )
    return event

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(event_data: EventCreate, db: AsyncSession = Depends(get_db)):
    """Створити нову подію"""
    event_service = EventService(db)
    try:
        return await event_service.create_event(event_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.put("/{event_id}", response_model=EventResponse)
async def update_event(event_id: int, event_data: EventUpdate, db: AsyncSession = Depends(get_db)):
    """Оновити подію"""
    event_service = EventService(db)
    try:
        updated_event = await event_service.update_event(event_id, event_data)
        if not updated_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with id {event_id} not found"
            )
        return updated_event
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db)):
    """Видалити подію"""
    event_service = EventService(db)
    deleted = await event_service.delete_event(event_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found"
        )

@router.get("/event/{event_id}", response_model=List[TicketResponse])
async def get_tickets_by_event(event_id: int, db: AsyncSession = Depends(get_db)):
    """Отримати квитки за ID події"""
    ticket_service = TicketService(db)
    tickets = await ticket_service.get_ticket_by_event(event_id)
    if not tickets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No tickets found for event with id {event_id}"
        )
    return tickets

@router.get("/with-artists/", response_model=List[EventWithArtistsResponse])
async def get_all_events_with_artists(db: AsyncSession = Depends(get_db)):
    """Отримати всі події з артистами (багато до багато)"""
    event_service = EventService(db)
    return await event_service.get_all_events_with_artists()
