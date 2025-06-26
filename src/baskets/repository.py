from abc import ABC, abstractmethod

from sqlalchemy import delete, select, update, insert
from sqlalchemy.orm import selectinload

from src.db.db import AsyncSessionDep
from src.models.models import Baskets
from src.utils.repository import SQLAlchemyRepository


class BasketsRepository(ABC): 
    @abstractmethod
    async def add(self, data: dict, session: AsyncSessionDep) -> int: ...

    @abstractmethod 
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[Baskets] | Baskets: ... 

    @abstractmethod 
    async def get_basket_with_products(self, user_id: int, session: AsyncSessionDep) -> Baskets: ... 

    @abstractmethod 
    async def increase_item_count(self, product_id: int, user_id: int, session: AsyncSessionDep) -> int: ...

    @abstractmethod
    async def decrease_item_count(self, product_id: int, user_id: int, session: AsyncSessionDep) -> int: ...

    @abstractmethod
    async def delete_product(self, product_id: int, user_id: int, session: AsyncSessionDep) -> int: ...

    @abstractmethod 
    async def clear_basket(self, user_id: int, session: AsyncSessionDep) -> None: ...


class PersistenceBasketsRepository(BasketsRepository):
    async def add(self, data: dict, session: AsyncSessionDep) -> int: 
        query = insert(Baskets).values(**data).returning(Baskets.id) 
        result = await session.execute(query) 
        return result.scalar() 
    
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[Baskets] | Baskets: 
        query = select(Baskets).filter_by(**filters) 
        result = await session.execute(query) 
        
        if one: 
            return result.scalar() 
        return result.scalars().all() 

    async def get_basket_with_products(self, user_id: int, session: AsyncSessionDep) -> Baskets:
        query = (
            select(Baskets)
            .where(Baskets.user_id == user_id)
            .options(selectinload(Baskets.product))
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def increase_item_count(self, product_id: int, user_id: int, session: AsyncSessionDep) -> int:
        query = (
            update(Baskets)
            .where(
                Baskets.product_id == product_id, Baskets.user_id == user_id
            )
            .values(quantity=Baskets.quantity + 1)
            .returning(Baskets.id)
        )
        result = await session.execute(query)
        return result.scalar()

    async def decrease_item_count(self, product_id: int, user_id: int, session: AsyncSessionDep) -> int:
        query = (
            update(Baskets)
            .where(
                Baskets.product_id == product_id, Baskets.user_id == user_id
            )
            .values(quantity=Baskets.quantity - 1)
            .returning(Baskets.id)
        )
        result = await session.execute(query)
        return result.scalar()

    async def delete_product(self, product_id: int, user_id: int, session: AsyncSessionDep) -> int:
        query = (
            delete(Baskets)
            .where(
                Baskets.product_id == product_id, Baskets.user_id == user_id
            )
            .returning(Baskets.id)
        )
        result = await session.execute(query)
        return result.scalar()

    async def clear_basket(self, user_id: int, session: AsyncSessionDep) -> None:
        query = delete(Baskets).where(Baskets.user_id == user_id)
        await session.execute(query)
