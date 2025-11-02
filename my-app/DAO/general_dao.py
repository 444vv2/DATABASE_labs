from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import Base

ModelType = TypeVar("ModelType")

class GeneralDAO(Generic[ModelType]):
    def __init__(self, session: AsyncSession):
        self.session = session

    def get_primary_key_name(self, model: Type[ModelType]) -> str:
        for column in model.__table__.columns:
            if column.primary_key:
                return column.name
        raise ValueError("No primary key found for the model.")

    async def get_all(self, model: Type[ModelType]) -> List[ModelType] | None:
        query = await self.session.execute(select(model))
        return query.scalars().all()

    async def get_by_id(self, model: Type[ModelType], pk_id: int) -> Optional[ModelType]:
        try:
            return await self.session.get(model, pk_id)
        except (ValueError, AttributeError) as e:
            print(f"Error occurred while fetching by ID: {e}")
            return None

    async def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: ModelType) -> ModelType:
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete_by_id(self, model: Type[ModelType], pk_id: int) -> bool:
        try:
            obj = await self.get_by_id(model, pk_id)
            if obj:
                await self.session.delete(obj)
                await self.session.commit()
                return True
            return False
        except (ValueError, AttributeError) as e:
            print(f"Error occurred while deleting by ID: {e}")
            return False
