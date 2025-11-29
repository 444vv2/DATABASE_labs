from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from DAO.general_dao import GeneralDAO
from db.models import Payment
from schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse


class PaymentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.general_dao = GeneralDAO[Payment](session)

    async def create_payment(self, payment_data: PaymentCreate) -> PaymentResponse:
        """Створення платежу"""
        new_payment = Payment(
            amount=payment_data.amount,
            payment_date=payment_data.payment_date,
            payment_type=payment_data.payment_type,
            is_paid=payment_data.is_paid,
            transaction_number=payment_data.transaction_number,
            order_id=payment_data.order_id
        )
        created_payment = await self.general_dao.create(new_payment)
        return PaymentResponse.model_validate(created_payment)

    async def get_payment_by_id(self, payment_id: int) -> Optional[PaymentResponse]:
        """Отримання платежу за ID"""
        payment = await self.general_dao.get_by_id(Payment, payment_id)
        if payment:
            return PaymentResponse.model_validate(payment)
        return None

    async def get_all_payments(self) -> list[PaymentResponse]:
        """Отримання всіх платежів"""
        payments = await self.general_dao.get_all(Payment)
        return [PaymentResponse.model_validate(payment) for payment in payments]

    async def get_payment_by_order(self, order_id: int) -> Optional[PaymentResponse]:
        """Отримання платежу за замовленням"""
        query = await self.session.execute(
            select(Payment).where(Payment.order_id == order_id)
        )
        payment = query.scalar_one_or_none()
        if payment:
            return PaymentResponse.model_validate(payment)
        return None

    async def update_payment(self, payment_id: int, payment_data: PaymentUpdate) -> Optional[PaymentResponse]:
        """Оновлення платежу"""
        payment = await self.general_dao.get_by_id(Payment, payment_id)
        if not payment:
            return None

        for field, value in payment_data.model_dump(exclude_unset=True).items():
            setattr(payment, field, value)

        updated_payment = await self.general_dao.update(payment)
        return PaymentResponse.model_validate(updated_payment)

    async def delete_payment_by_id(self, payment_id: int) -> bool:
        """Видалення платежу за ID"""
        return await self.general_dao.delete_by_id(Payment, payment_id)

    async def mark_as_paid(self, payment_id: int) -> Optional[PaymentResponse]:
        """Позначити платіж як оплачений"""
        payment = await self.general_dao.get_by_id(Payment, payment_id)
        if not payment:
            return None

        payment.is_paid = True
        updated_payment = await self.general_dao.update(payment)
        return PaymentResponse.model_validate(updated_payment)
