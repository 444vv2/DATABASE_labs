from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from DAO.general_dao import GeneralDAO
from db.models import Delivery
from schemas.delivery import DeliveryCreate, DeliveryUpdate, DeliveryResponse


class DeliveryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.general_dao = GeneralDAO[Delivery](session)

    async def create_delivery(self, delivery_data: DeliveryCreate) -> DeliveryResponse:
        """Створення доставки"""
        new_delivery = Delivery(
            delivery_type=delivery_data.delivery_type,
            delivery_time=delivery_data.delivery_time,
            is_delivered=delivery_data.is_delivered,
            order_id=delivery_data.order_id
        )
        created_delivery = await self.general_dao.create(new_delivery)
        return DeliveryResponse.model_validate(created_delivery)

    async def get_delivery_by_id(self, delivery_id: int) -> Optional[DeliveryResponse]:
        """Отримання доставки за ID"""
        delivery = await self.general_dao.get_by_id(Delivery, delivery_id)
        if delivery:
            return DeliveryResponse.model_validate(delivery)
        return None

    async def get_delivery_by_order(self, order_id: int) -> Optional[DeliveryResponse]:
        """Отримання доставки за замовленням"""
        query = await self.session.execute(
            select(Delivery).where(Delivery.order_id == order_id)
        )
        delivery = query.scalar_one_or_none()
        if delivery:
            return DeliveryResponse.model_validate(delivery)
        return None

    async def update_delivery(self, delivery_id: int, delivery_data: DeliveryUpdate) -> Optional[DeliveryResponse]:
        """Оновлення доставки"""
        delivery = await self.general_dao.get_by_id(Delivery, delivery_id)
        if not delivery:
            return None

        for field, value in delivery_data.model_dump(exclude_unset=True).items():
            setattr(delivery, field, value)

        updated_delivery = await self.general_dao.update(delivery)
        return DeliveryResponse.model_validate(updated_delivery)

    async def mark_as_delivered(self, delivery_id: int) -> Optional[DeliveryResponse]:
        """Позначити як доставлено"""
        delivery = await self.general_dao.get_by_id(Delivery, delivery_id)
        if not delivery:
            return None

        delivery.is_delivered = True
        updated_delivery = await self.general_dao.update(delivery)
        return DeliveryResponse.model_validate(updated_delivery)

    async def get_deliveries_by_type(self, delivery_type: str) -> List[DeliveryResponse]:
        """Отримання доставок за типом"""
        query = await self.session.execute(
            select(Delivery).where(Delivery.delivery_type == delivery_type)
        )
        deliveries = query.scalars().all()
        return [DeliveryResponse.model_validate(delivery) for delivery in deliveries]

    async def get_all_deliveries(self) -> List[DeliveryResponse]:
        """Отримання всіх доставок"""
        deliveries = await self.general_dao.get_all(Delivery)
        return [DeliveryResponse.model_validate(delivery) for delivery in deliveries]

    async def delete_delivery(self, delivery_id: int) -> bool:
        """Видалення доставки за ID"""
        result = await self.general_dao.delete_by_id(Delivery, delivery_id)
        return result
