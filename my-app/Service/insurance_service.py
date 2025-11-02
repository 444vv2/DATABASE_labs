from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from DAO.general_dao import GeneralDAO
from db.models import Insurance
from schemas.insurance import InsuranceCreate, InsuranceUpdate, InsuranceResponse


class InsuranceService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.general_dao = GeneralDAO[Insurance](session)

    async def create_insurance(self, insurance_data: InsuranceCreate) -> InsuranceResponse:
        """Створення страхівки"""
        new_insurance = Insurance(
            country_travel=insurance_data.country_travel,
            starting_time=insurance_data.starting_time,
            finish_time=insurance_data.finish_time,
            number_tourist=insurance_data.number_tourists,
            price=insurance_data.price,
            order_id=insurance_data.order_id
        )
        created_insurance = await self.general_dao.create(new_insurance)
        return InsuranceResponse.model_validate(created_insurance)

    async def get_insurance_by_id(self, insurance_id: int) -> Optional[InsuranceResponse]:
        """Отримання страхівки за ID"""
        insurance = await self.general_dao.get_by_id(Insurance, insurance_id)
        if insurance:
            return InsuranceResponse.model_validate(insurance)
        return None

    async def get_insurance_by_order(self, order_id: int) -> Optional[InsuranceResponse]:
        """Отримання страхівки за замовленням"""
        query = await self.session.execute(
            select(Insurance).where(Insurance.order_id == order_id)
        )
        insurance = query.scalar_one_or_none()
        if insurance:
            return InsuranceResponse.model_validate(insurance)
        return None

    async def update_insurance(self, insurance_id: int, insurance_data: InsuranceUpdate) -> Optional[InsuranceResponse]:
        """Оновлення страхівки"""
        insurance = await self.general_dao.get_by_id(Insurance, insurance_id)
        if not insurance:
            return None

        for field, value in insurance_data.model_dump(exclude_unset=True).items():
            setattr(insurance, field, value)

        updated_insurance = await self.general_dao.update(insurance)
        return InsuranceResponse.model_validate(updated_insurance)

    async def get_insurances_by_country(self, country: str) -> List[InsuranceResponse]:
        """Отримання страхівок за країною"""
        query = await self.session.execute(
            select(Insurance).where(Insurance.country_travel.ilike(f"%{country}%"))
        )
        insurances = query.scalars().all()
        return [InsuranceResponse.model_validate(insurance) for insurance in insurances]
