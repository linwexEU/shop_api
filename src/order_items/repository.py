from abc import ABC, abstractmethod

from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload

from src.db.db import AsyncSessionDep
from src.models.models import OrderItems
from src.utils.repository import SQLAlchemyRepository


class OrderItemsRepository(ABC): 
    @abstractmethod
    async def add(self, data: dict, session: AsyncSessionDep) -> int: ...

    @abstractmethod 
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[OrderItems] | OrderItems: ... 

    @abstractmethod 
    async def get_full_order_items(self, user_id: int, session: AsyncSessionDep) -> OrderItems: ...


class PersistenceOrderItemsRepository(OrderItemsRepository):
    async def add(self, data: dict, session: AsyncSessionDep) -> int: 
        query = insert(OrderItems).values(**data).returning(OrderItems.id) 
        result = await session.execute(query) 
        return result.scalar() 
    
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[OrderItems] | OrderItems: 
        query = select(OrderItems).filter_by(**filters) 
        result = await session.execute(query) 
        
        if one: 
            return result.scalar() 
        return result.scalars().all() 

    async def get_full_order_items(self, user_id: int, session: AsyncSessionDep) -> OrderItems:
        query = (
            select(OrderItems)
            .where(OrderItems.user_id == user_id)
            .options(
                selectinload(OrderItems.order), selectinload(OrderItems.product)
            )
        )
        result = await session.execute(query)
        return result.scalars().all()
