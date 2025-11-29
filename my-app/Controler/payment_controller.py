from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_db
from Service import PaymentService
from schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(payment_data: PaymentCreate, db: AsyncSession = Depends(get_db)):
    """Створення нового платежу"""
    payment_service = PaymentService(db)
    try:
        payment = await payment_service.create_payment(payment_data)
        return payment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment_by_id(payment_id: int, db: AsyncSession = Depends(get_db)):
    """Отримання платежу за ID"""
    payment_service = PaymentService(db)
    payment = await payment_service.get_payment_by_id(payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payment with id {payment_id} not found"
        )
    return payment

@router.get("/", response_model=List[PaymentResponse])
async def get_all_payments(db: AsyncSession = Depends(get_db)):
    """Отримання всіх платежів"""
    payment_service = PaymentService(db)
    payments = await payment_service.get_all_payments()
    return payments

@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(payment_id: int, payment_data: PaymentUpdate, db: AsyncSession = Depends(get_db)):
    """Оновлення платежу"""
    payment_service = PaymentService(db)
    try:
        payment = await payment_service.update_payment(payment_id, payment_data)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment with id {payment_id} not found"
            )
        return payment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(payment_id: int, db: AsyncSession = Depends(get_db)):
    """Видалення платежу"""
    payment_service = PaymentService(db)
    try:
        deleted = await payment_service.delete_payment_by_id(payment_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment with id {payment_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
