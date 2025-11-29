from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_db
from Service import ProcedureService

router = APIRouter(prefix="/procedure", tags=["procedure"])

@router.post("/create_dbs_with_tables", status_code=status.HTTP_200_OK)
async def create_dbs_with_tables(db: AsyncSession = Depends(get_db)):
    """Створити бази даних з таблицями за допомогою процедури"""
    procedure_service = ProcedureService(db)
    try:
        await procedure_service.create_dbs_with_tables()
        return {"detail": "Databases with tables created successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.delete("/drop_dbs_with_tables", status_code=status.HTTP_200_OK)
async def drop_dbs_with_tables(db: AsyncSession = Depends(get_db)):
    """Видалити створені бази даних з таблицями за допомогою процедури"""
    procedure_service = ProcedureService(db)
    try:
        await procedure_service.drop_dbs_with_tables()
        return {"detail": "Databases with tables dropped successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
