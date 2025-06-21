from sqlalchemy import delete, select, update
from sqlalchemy.orm import selectinload

from src.db.db import async_session_maker
from src.models.models import Baskets
from src.utils.repository import SQLAlchemyRepository


class BasketsRepository(SQLAlchemyRepository):
    model = Baskets

    async def get_basket_with_products(self, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(self.model)
                .where(self.model.user_id == user_id)
                .options(selectinload(self.model.product))
            )
            result = await session.execute(query)
            return result.scalars().all()

    async def increase_item_count(self, product_id: int, user_id: int) -> int:
        async with async_session_maker() as session:
            query = (
                update(self.model)
                .where(
                    self.model.product_id == product_id, self.model.user_id == user_id
                )
                .values(quantity=self.model.quantity + 1)
                .returning(self.model.id)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    async def decrease_item_count(self, product_id: int, user_id: int) -> int:
        async with async_session_maker() as session:
            query = (
                update(self.model)
                .where(
                    self.model.product_id == product_id, self.model.user_id == user_id
                )
                .values(quantity=self.model.quantity - 1)
                .returning(self.model.id)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    async def delete_product(self, product_id: int, user_id: int) -> int:
        async with async_session_maker() as session:
            query = (
                delete(self.model)
                .where(
                    self.model.product_id == product_id, self.model.user_id == user_id
                )
                .returning(self.model.id)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    async def clear_basket(self, user_id: int) -> None:
        async with async_session_maker() as session:
            query = delete(self.model).where(self.model.user_id == user_id)
            await session.execute(query)
            await session.commit()
