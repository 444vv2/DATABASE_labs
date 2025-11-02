from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User


class UserDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        query = await self.session.execute(select(User).where(User.email == email))
        return query.scalar_one_or_none()

    async def get_by_phone(self, phone: str) -> Optional[User]:
        query = await self.session.execute(select(User).where(User.phone == phone))
        return query.scalar_one_or_none()

    async def get_user_with_orders(self, user_id: int) -> Optional[User]:
        query = await self.session.execute(
            select(User).where(User.user_id == user_id).options(selectinload(User.orders))
        )
        return query.scalar_one_or_none()
