from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_db
from Service import PaymentService
from schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(payment_data: PaymentCreate, db: AsyncSession = Depends(get_db)):
    try:
        payment = await PaymentService.create_payment(db, payment_data)
        return payment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment_by_id(payment_id: int, db: AsyncSession = Depends(get_db)):
    payment = await PaymentService.get_payment_by_id(db, payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payment with id {payment_id} not found"
        )
    return payment

@router.get("/", response_model=List[PaymentResponse])
async def get_all_payments(db: AsyncSession = Depends(get_db)):
    payments = await PaymentService.get_all_payments(db)
    return payments

@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(payment_id: int, payment_data: PaymentUpdate, db: AsyncSession = Depends(get_db)):
    try:
        payment = await PaymentService.update_payment(db, payment_id, payment_data)
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
    try:
        deleted = await PaymentService.delete_payment_by_id(db, payment_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment with id {payment_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
