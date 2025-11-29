from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text

class ProcedureService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_dbs_with_tables(self) -> None:
        try:
            await self.session.execute(
                text("CALL create_dbs_with_tables()")
            )
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e from e

    async def drop_dbs_with_tables(self) -> None:
        try:
            await self.session.execute(
                text("CALL drop_created_dbs()")
            )
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e from e
