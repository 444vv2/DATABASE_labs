from typing import Optional, List
import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from DAO.user_dao import UserDAO
from DAO.general_dao import GeneralDAO
from db.models import User, UserPassword
from schemas.user import UserCreate, UserUpdate, UserResponse


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_dao = UserDAO(session)
        self.general_dao = GeneralDAO[User](session)
        self.password_dao = GeneralDAO[UserPassword](session)

    def _hash_password(self, password: str) -> str:
        """Хешування пароля"""
        return hashlib.sha256(password.encode()).hexdigest()

    async def create_user_with_password(self, user_data: UserCreate) -> UserResponse:
        """
        Створення користувача з паролем
        Бізнес-логіка: перевірка на дублікати, хешування пароля
        """
        try:
            existing_user = await self.user_dao.get_by_email(user_data.email)
            if existing_user:
                raise ValueError(f"User with email {user_data.email} already exists")

            existing_phone = await self.user_dao.get_by_phone(user_data.phone)
            if existing_phone:
                raise ValueError(f"User with phone {user_data.phone} already exists")

            new_user = User(
                name=user_data.name,
                surname=user_data.surname,
                phone=user_data.phone,
                email=user_data.email
            )
            created_user = await self.general_dao.create(new_user)

            # 4. Створюємо запис пароля
            hashed_password = self._hash_password(user_data.password)
            user_password = UserPassword(
                user_id=created_user.user_id,
                password_hash=hashed_password
            )
            await self.password_dao.create(user_password)

            return UserResponse.model_validate(created_user)

        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError(f"Database integrity error: {str(e)}") from e
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Отримання користувача по ID"""
        user = await self.general_dao.get_by_id(User, user_id)
        if not user:
            return None
        return UserResponse.model_validate(user)

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Отримання користувача по email"""
        user = await self.user_dao.get_by_email(email)
        if not user:
            return None
        return UserResponse.model_validate(user)

    async def get_all_users(self) -> List[UserResponse]:
        """Отримання всіх користувачів"""
        users = await self.general_dao.get_all(User)
        return [UserResponse.model_validate(user) for user in users]

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        """
        Оновлення користувача  
        Бізнес-логіка: перевірка унікальності email/phone при оновленні
        """
        try:
            # 1. Знаходимо користувача
            user = await self.general_dao.get_by_id(User, user_id)
            if not user:
                return None

            # 2. Перевіряємо унікальність email (якщо змінюється)
            if user_data.email and user_data.email != user.email:
                existing_email = await self.user_dao.get_by_email(user_data.email)
                if existing_email:
                    raise ValueError(f"Email {user_data.email} already exists")

            # 3. Перевіряємо унікальність phone (якщо змінюється)
            if user_data.phone and user_data.phone != user.phone:
                existing_phone = await self.user_dao.get_by_phone(user_data.phone)
                if existing_phone:
                    raise ValueError(f"Phone {user_data.phone} already exists")

            # 4. Оновлюємо поля
            if user_data.name is not None:
                user.name = user_data.name
            if user_data.surname is not None:
                user.surname = user_data.surname
            if user_data.email is not None:
                user.email = user_data.email
            if user_data.phone is not None:
                user.phone = user_data.phone

            # 5. Зберігаємо зміни
            updated_user = await self.general_dao.update(user)
            return UserResponse.model_validate(updated_user)

        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete_user(self, user_id: int) -> bool:
        """
        Видалення користувача
        Бізнес-логіка: видаляємо User + UserPassword
        """
        try:
            # 1. Перевіряємо чи користувач існує
            user = await self.general_dao.get_by_id(User, user_id)
            if not user:
                return False

            # 2. Видаляємо пароль (якщо є)
            if user.password:
                await self.password_dao.delete_by_id(UserPassword, user_id)
            # 3. Видаляємо користувача
            result = await self.general_dao.delete_by_id(User, user_id)
            return result

        except Exception as e:
            await self.session.rollback()
            raise e

    async def authenticate_user(self, email: str, password: str) -> Optional[UserResponse]:
        """
        Аутентифікація користувача
        Бізнес-логіка: перевірка пароля
        """
        # 1. Знаходимо користувача
        user = await self.user_dao.get_by_email(email)
        if not user:
            return None

        # 2. Отримуємо хеш пароля з БД
        query = await self.session.execute(
            select(UserPassword).where(UserPassword.user_id == user.user_id)
        )
        user_password = query.scalar_one_or_none()

        if not user_password:
            return None

        # 3. Перевіряємо пароль
        input_hash = self._hash_password(password)
        if input_hash != user_password.password_hash:
            return None

        return UserResponse.model_validate(user)

    async def get_user_with_orders(self, user_id: int) -> Optional[UserResponse]:
        """Отримання користувача разом з його замовленнями"""
        user = await self.user_dao.get_user_with_orders(user_id)
        if not user:
            return None
        return UserResponse.model_validate(user)
