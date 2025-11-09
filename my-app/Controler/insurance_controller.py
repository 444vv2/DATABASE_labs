from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_db
from Service import InsuranceService
from schemas.insurance import InsuranceCreate, InsuranceUpdate, InsuranceResponse

router = APIRouter(prefix="/insurances", tags=["insurances"])

@router.post("/", response_model=InsuranceResponse, status_code=status.HTTP_201_CREATED)
async def create_insurance(insurance_data: InsuranceCreate, db: AsyncSession = Depends(get_db)):
    """Створення нового страхування"""
    insurance_service = InsuranceService(db)
    try:
        insurance = await insurance_service.create_insurance(insurance_data)
        return insurance
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.get("/{insurance_id}", response_model=InsuranceResponse)
async def get_insurance_by_id(insurance_id: int, db: AsyncSession = Depends(get_db)):
    """Отримання страхування за ID"""
    insurance_service = InsuranceService(db)
    insurance = await insurance_service.get_insurance_by_id(insurance_id)
    if not insurance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Insurance with id {insurance_id} not found"
        )
    return insurance

@router.get("/", response_model=List[InsuranceResponse])
async def get_all_insurances(db: AsyncSession = Depends(get_db)):
    """Отримання всіх страхувань"""
    insurance_service = InsuranceService(db)
    insurances = await insurance_service.get_all_insurances()
    return insurances

@router.put("/{insurance_id}", response_model=InsuranceResponse)
async def update_insurance(insurance_id: int, insurance_data: InsuranceUpdate, db: AsyncSession = Depends(get_db)):
    """Оновлення страхування"""
    insurance_service = InsuranceService(db)
    try:
        insurance = await insurance_service.update_insurance(insurance_id, insurance_data)
        if not insurance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Insurance with id {insurance_id} not found"
            )
        return insurance
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.delete("/{insurance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_insurance(insurance_id: int, db: AsyncSession = Depends(get_db)):
    """Видалення страхування"""
    insurance_service = InsuranceService(db)
    try:
        deleted = await insurance_service.delete_insurance_by_id(insurance_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Insurance with id {insurance_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
