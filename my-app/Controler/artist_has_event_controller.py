from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_db
from Service import ArtistHasEventService
from schemas.artist_has_event import ArtistHasEventCreate, ArtistHasEventResponse

router = APIRouter(prefix="/artist_has_event", tags=["artist_has_event"])

@router.post("/ArtistHasEvent", response_model=ArtistHasEventResponse, status_code=status.HTTP_201_CREATED)
async def create_by_name_surname_and_title(artist_event_data: ArtistHasEventCreate, db: AsyncSession = Depends(get_db)):
    service = ArtistHasEventService(db)
    try:
        artist_event = await service.create_by_name_surname_and_title(
            artist_name=artist_event_data.artist_name,
            artist_surname=artist_event_data.artist_surname,
            event_name=artist_event_data.event_name,
        )
        return artist_event
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        ) from ve
