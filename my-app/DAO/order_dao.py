from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Order

class OrderDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_orders_by_user(self, user_id: int) -> list[Order]:
        query = await self.session.execute(select(Order).where(Order.user_id == user_id))
        return query.scalars().all()
