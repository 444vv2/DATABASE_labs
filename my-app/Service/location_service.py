from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from DAO.general_dao import GeneralDAO
from db.models import Location
from schemas.location import LocationCreate, LocationUpdate, LocationResponse


class LocationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.general_dao = GeneralDAO[Location](session)

    async def create_location(self, location_data: LocationCreate) -> LocationResponse:
        """Створення локації"""
        new_location = Location(
            city=location_data.city,
            country=location_data.country
        )
        created_location = await self.general_dao.create(new_location)
        return LocationResponse.model_validate(created_location)

    async def get_location_by_id(self, location_id: int) -> Optional[LocationResponse]:
        """Отримання локації за ID"""
        location = await self.general_dao.get_by_id(Location, location_id)
        if location:
            return LocationResponse.model_validate(location)
        return None

    async def get_all_locations(self) -> List[LocationResponse]:
        """Отримання всіх локацій"""
        locations = await self.general_dao.get_all(Location)
        return [LocationResponse.model_validate(location) for location in locations]

    async def update_location(self, location_id: int, location_data: LocationUpdate) -> Optional[LocationResponse]:
        """Оновлення локації"""
        location = await self.general_dao.get_by_id(Location, location_id)
        if not location:
            return None

        for field, value in location_data.model_dump(exclude_unset=True).items():
            setattr(location, field, value)

        updated_location = await self.general_dao.update(location)
        return LocationResponse.model_validate(updated_location)

    async def delete_location(self, location_id: int) -> bool:
        """Видалення локації"""
        return await self.general_dao.delete_by_id(Location, location_id)

    async def get_location_by_city(self, city: str) -> List[LocationResponse]:
        """Пошук локацій за містом"""
        query = await self.session.execute(
            select(Location).where(Location.city.ilike(f"%{city}%"))
        )
        locations = query.scalars().all()
        return [LocationResponse.model_validate(location) for location in locations]

    async def get_location_by_country(self, country: str) -> List[LocationResponse]:
        """Пошук локацій за країною"""
        query = await self.session.execute(
            select(Location).where(Location.country.ilike(f"%{country}%"))
        )
        locations = query.scalars().all()
        return [LocationResponse.model_validate(location) for location in locations]
