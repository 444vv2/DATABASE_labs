from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from DAO.order_dao import OrderDAO
from DAO.general_dao import GeneralDAO
from db.models import Order
from schemas.order import OrderCreate, OrderUpdate, OrderResponse


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_dao = OrderDAO(session)
        self.general_dao = GeneralDAO[Order](session)

    async def create_order(self, order_data: OrderCreate) -> OrderResponse:
        """
        Створення замовлення
        """
        new_order = Order(
            user_id=order_data.user_id,
            order_date=order_data.order_date,
            payment_status=order_data.payment_status,
            ticket_type=order_data.ticket_type,
            delivery_type=order_data.delivery_type
        )
        created_order = await self.general_dao.create(new_order)
        return OrderResponse.model_validate(created_order)

    async def get_order_by_id(self, order_id: int) -> Optional[OrderResponse]:
        """
        Отримання замовлення за ID
        """
        order = await self.general_dao.get_by_id(Order, order_id)
        if order:
            return OrderResponse.model_validate(order)
        return None

    async def update_order(self, order_id: int, order_data: OrderUpdate) -> Optional[OrderResponse]:
        """
        Оновлення інформації про замовлення
        """
        order = await self.general_dao.get_by_id(Order, order_id)
        if not order:
            return None

        for field, value in order_data.model_dump(exclude_unset=True).items():
            setattr(order, field, value)

        updated_order = await self.general_dao.update(order)
        return OrderResponse.model_validate(updated_order)

    async def delete_order(self, order_id: int) -> bool:
        """
        Видалення замовлення за ID
        """
        return await self.general_dao.delete_by_id(Order, order_id)

    async def get_all_orders(self) -> List[OrderResponse]:
        """
        Отримання всіх замовлень
        """
        orders = await self.general_dao.get_all(Order)
        return [OrderResponse.model_validate(order) for order in orders]

    async def get_orders_by_user(self, user_id: int) -> List[OrderResponse]:
        """
        Отримання всіх замовлень користувача
        """
        orders = await self.order_dao.get_orders_by_user(user_id)
        return [OrderResponse.model_validate(order) for order in orders]

    async def create_orders_for_user(self, user_id: int, orders_data: OrderCreate) -> Optional[OrderResponse]:
        """
        Створення замовлень для користувача
        """
        new_order = Order(
            user_id=user_id,
            order_date=orders_data.order_date,
            payment_status=orders_data.payment_status,
            ticket_type=orders_data.ticket_type,
            delivery_type=orders_data.delivery_type
        )
        created_order = await self.general_dao.create(new_order)
        return OrderResponse.model_validate(created_order)

    async def update_delivery_type(self, order_id: int, delivery_type: str) -> Optional[OrderResponse]:
        """
        Оновлення типу доставки замовлення
        """
        order = await self.general_dao.get_by_id(Order, order_id)
        if not order:
            return None

        order.delivery_type = delivery_type
        updated_order = await self.general_dao.update(order)
        return OrderResponse.model_validate(updated_order)

    async def get_orders_by_delivery_type(self, delivery_type: str) -> List[OrderResponse]:
        """
        Отримання замовлень за типом доставки
        """
        query = await self.session.execute(
            select(Order).where(Order.delivery_type == delivery_type)
        )
        orders = query.scalars().all()
        return [OrderResponse.model_validate(order) for order in orders]

    async def get_orders_by_ticket_type(self, ticket_type: str) -> List[OrderResponse]:
        """
        Отримання замовлень за типом квитка
        """
        query = await self.session.execute(
            select(Order).where(Order.ticket_type == ticket_type)
        )
        orders = query.scalars().all()
        return [OrderResponse.model_validate(order) for order in orders]

    async def cancel_order(self, order_id: int) -> Optional[OrderResponse]:
        """
        Скасування замовлення
        """
        order = await self.general_dao.get_by_id(Order, order_id)
        if not order:
            return None

        order.payment_status = "canceled"
        updated_order = await self.general_dao.update(order)
        return OrderResponse.model_validate(updated_order)
