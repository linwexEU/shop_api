from abc import ABC, abstractmethod

from sqlalchemy import update, select, insert

from src.db.db import AsyncSessionDep
from src.models.models import ProductRates


class ProductRatesRepository(ABC): 
    @abstractmethod
    async def add(self, data: dict, session: AsyncSessionDep) -> int: ...

    @abstractmethod 
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[ProductRates] | ProductRates: ... 

    @abstractmethod 
    async def like_rate(self, rate_id: int, user_id: int, session: AsyncSessionDep) -> int: ... 

    @abstractmethod 
    async def dislike_rate(self, rate_id: int, user_id: int, session: AsyncSessionDep) -> int: ... 

    @abstractmethod 
    async def remove_like_rate(self, rate_id: int, session: AsyncSessionDep) -> int: ... 

    @abstractmethod 
    async def remove_dislike_rate(self, rate_id: int, session: AsyncSessionDep) -> int: ...


class PersistenceProductRatesRepository(ProductRatesRepository):
    async def add(self, data: dict, session: AsyncSessionDep) -> int: 
        query = insert(ProductRates).values(**data).returning(ProductRates.id) 
        result = await session.execute(query) 
        return result.scalar() 
    
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[ProductRates] | ProductRates: 
        query = select(ProductRates).filter_by(**filters) 
        result = await session.execute(query) 
        
        if one: 
            return result.scalar() 
        return result.scalars().all() 

    async def like_rate(self, rate_id: int, user_id: int, session: AsyncSessionDep) -> int:
        query = (
            update(ProductRates)
            .where(ProductRates.id == rate_id, ProductRates.user_id != user_id)
            .values(likes=ProductRates.likes + 1)
            .returning(ProductRates.id)
        )
        result = await session.execute(query)
        return result.scalar()

    async def dislike_rate(self, rate_id: int, user_id: int, session: AsyncSessionDep) -> int:
        query = (
            update(ProductRates)
            .where(ProductRates.id == rate_id, ProductRates.user_id != user_id)
            .values(dislikes=ProductRates.dislikes + 1)
            .returning(ProductRates.id)
        )
        result = await session.execute(query)
        return result.scalar()

    async def remove_like_rate(self, rate_id: int, session: AsyncSessionDep) -> int:
        query = (
            update(ProductRates)
            .where(ProductRates.id == rate_id)
            .values(likes=ProductRates.likes - 1)
            .returning(ProductRates.id)
        )
        result = await session.execute(query)
        return result.scalar()

    async def remove_dislike_rate(self, rate_id: int, session: AsyncSessionDep) -> int:
        query = (
            update(ProductRates)
            .where(ProductRates.id == rate_id)
            .values(dislikes=ProductRates.dislikes - 1)
            .returning(ProductRates.id)
        )
        result = await session.execute(query)
        return result.scalar()
