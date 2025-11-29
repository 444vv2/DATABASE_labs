from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text

from db.models import ArtistHasEvent
from schemas.artist_has_event import ArtistHasEventResponse

class ArtistHasEventService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_by_name_surname_and_title(self, artist_name: str, artist_surname: str, event_name: str) -> ArtistHasEventResponse:
        try:
            await self.session.execute(
                text("CALL ArtistHasEvent(:artist_name, :artist_surname, :event_name)"),
                {"artist_name": artist_name, "artist_surname": artist_surname, "event_name": event_name}
            )
            await self.session.commit()

            artist_result = await self.session.execute(
                text("SELECT artist_id FROM artist WHERE name = :name AND surname = :surname LIMIT 1"),
                {"name": artist_name, "surname": artist_surname}
            )
            artist_row = artist_result.fetchone()

            event_result = await self.session.execute(
                text("SELECT event_id FROM event WHERE title = :title LIMIT 1"),
                {"title": event_name}
            )
            event_row = event_result.fetchone()

            if not artist_row or not event_row:
                raise ValueError("Could not find created artist-event relationship")

            result = await self.session.execute(
                select(ArtistHasEvent).where(
                    ArtistHasEvent.artist_id == artist_row[0],
                    ArtistHasEvent.event_id == event_row[0]
                )
            )
            artist_has_event = result.scalars().first()

            if not artist_has_event:
                raise ValueError("Failed to create ArtistHasEvent")

            return ArtistHasEventResponse.model_validate(artist_has_event)

        except Exception as e:
            await self.session.rollback()
            error_msg = str(e)
            if "Duplicate entry" in error_msg and "PRIMARY" in error_msg:
                raise ValueError(f"Artist '{artist_name} {artist_surname}' is already linked to event '{event_name}'") from e
            elif "This artist does not exist" in error_msg:
                raise ValueError(f"Artist '{artist_name} {artist_surname}' does not exist") from e
            elif "This event does not exist" in error_msg:
                raise ValueError(f"Event '{event_name}' does not exist") from e
            else:
                raise ValueError(f"Error creating ArtistHasEvent: {error_msg}") from e
