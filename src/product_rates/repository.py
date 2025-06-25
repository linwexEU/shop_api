from sqlalchemy import update

from src.db.db import async_session_maker
from src.models.models import ProductRates
from src.utils.repository import SQLAlchemyRepository


class ProductRatesRepository(SQLAlchemyRepository):
    model = ProductRates

    async def like_rate(self, rate_id: int, user_id: int) -> int:
        async with async_session_maker() as session:
            query = (
                update(self.model)
                .where(self.model.id == rate_id, self.model.user_id != user_id)
                .values(likes=self.model.likes + 1)
                .returning(self.model.id)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    async def dislike_rate(self, rate_id: int, user_id: int) -> int:
        async with async_session_maker() as session:
            query = (
                update(self.model)
                .where(self.model.id == rate_id, self.model.user_id != user_id)
                .values(dislikes=self.model.dislikes + 1)
                .returning(self.model.id)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    async def remove_like_rate(self, rate_id: int) -> int:
        async with async_session_maker() as session:
            query = (
                update(self.model)
                .where(self.model.id == rate_id)
                .values(likes=self.model.likes - 1)
                .returning(self.model.id)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    async def remove_dislike_rate(self, rate_id: int) -> int:
        async with async_session_maker() as session:
            query = (
                update(self.model)
                .where(self.model.id == rate_id)
                .values(dislikes=self.model.dislikes - 1)
                .returning(self.model.id)
            )
            result = await session.execute(query)
            await session.commit(query)
            return result.scalar()
