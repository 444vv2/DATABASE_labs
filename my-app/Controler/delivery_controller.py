from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_db
from Service import DeliveryService
from schemas.delivery import DeliveryCreate, DeliveryUpdate, DeliveryResponse

router = APIRouter(prefix="/deliveries", tags=["deliveries"])

@router.get("/", response_model=List[DeliveryResponse])
async def get_all_deliveries(db: AsyncSession = Depends(get_db)):
    """Отримати всі доставки"""
    delivery_service = DeliveryService(db)
    return await delivery_service.get_all_deliveries()

@router.get("/{delivery_id}", response_model=DeliveryResponse)
async def get_delivery_by_id(delivery_id: int, db: AsyncSession = Depends(get_db)):
    """Отримати доставку за ID"""
    delivery_service = DeliveryService(db)
    delivery = await delivery_service.get_delivery_by_id(delivery_id)
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Delivery with id {delivery_id} not found"
        )
    return delivery

@router.post("/", response_model=DeliveryResponse, status_code=status.HTTP_201_CREATED)
async def create_delivery(delivery_data: DeliveryCreate, db: AsyncSession = Depends(get_db)):
    """Створити нову доставку"""
    delivery_service = DeliveryService(db)
    return await delivery_service.create_delivery(delivery_data)

@router.put("/{delivery_id}", response_model=DeliveryResponse)
async def update_delivery(delivery_id: int, delivery_data: DeliveryUpdate, db: AsyncSession = Depends(get_db)):
    """Оновити доставку"""
    delivery_service = DeliveryService(db)
    updated_delivery = await delivery_service.update_delivery(delivery_id, delivery_data)
    if not updated_delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Delivery with id {delivery_id} not found"
        )
    return updated_delivery

@router.delete("/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_delivery(delivery_id: int, db: AsyncSession = Depends(get_db)):
    """Видалити доставку"""
    delivery_service = DeliveryService(db)
    try:
        await delivery_service.delete_delivery(delivery_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
