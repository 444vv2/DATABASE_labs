from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from DAO.general_dao import GeneralDAO
from db.models import Artist
from schemas.artist import ArtistCreate, ArtistUpdate, ArtistResponse


class ArtistService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.general_dao = GeneralDAO[Artist](session)

    async def create_artist(self, artist_data: ArtistCreate) -> ArtistResponse:
        """Створення артиста"""
        new_artist = Artist(
            name=artist_data.name,
            surname=artist_data.surname,
            nickname=artist_data.nickname,
            genre=artist_data.genre,
            is_group=artist_data.is_group
        )
        created_artist = await self.general_dao.create(new_artist)
        return ArtistResponse.model_validate(created_artist)

    async def get_artist_by_id(self, artist_id: int) -> Optional[ArtistResponse]:
        """Отримання артиста за ID"""
        artist = await self.general_dao.get_by_id(Artist, artist_id)
        if artist:
            return ArtistResponse.model_validate(artist)
        return None

    async def get_all_artists(self) -> List[ArtistResponse]:
        """Отримання всіх артистів"""
        artists = await self.general_dao.get_all(Artist)
        return [ArtistResponse.model_validate(artist) for artist in artists]

    async def update_artist(self, artist_id: int, artist_data: ArtistUpdate) -> Optional[ArtistResponse]:
        """Оновлення артиста"""
        artist = await self.general_dao.get_by_id(Artist, artist_id)
        if not artist:
            return None

        for field, value in artist_data.model_dump(exclude_unset=True).items():
            setattr(artist, field, value)

        updated_artist = await self.general_dao.update(artist)
        return ArtistResponse.model_validate(updated_artist)

    async def delete_artist_by_id(self, artist_id: int) -> bool:
        """Видалення артиста за ID"""
        return await self.general_dao.delete_by_id(Artist, artist_id)

    async def search_artists(self, search_term: str) -> List[ArtistResponse]:
        """Пошук артистів за ім'ям, прізвищем або псевдонімом"""
        query = await self.session.execute(
            select(Artist).where(
                or_(
                    Artist.name.ilike(f"%{search_term}%"),
                    Artist.surname.ilike(f"%{search_term}%"),
                    Artist.nickname.ilike(f"%{search_term}%")
                )
            )
        )
        artists = query.scalars().all()
        return [ArtistResponse.model_validate(artist) for artist in artists]
