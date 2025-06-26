from abc import ABC, abstractmethod
from datetime import datetime, timezone

from sqlalchemy import update, select, insert

from src.db.db import AsyncSessionDep
from src.models.enums import OrdersStateEnum
from src.models.models import Orders


class OrdersRepository(ABC): 
    @abstractmethod
    async def add(self, data: dict, session: AsyncSessionDep) -> int: ...

    @abstractmethod 
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[Orders] | Orders: ... 

    @abstractmethod 
    async def update_state(self, uuid: str, state: OrdersStateEnum, session: AsyncSessionDep) -> int: ... 

    @abstractmethod 
    async def canceled_order(self, uuid: str, session: AsyncSessionDep) -> int: ...


class PersistenceOrdersRepository(OrdersRepository):
    async def add(self, data: dict, session: AsyncSessionDep) -> int: 
        query = insert(Orders).values(**data).returning(Orders.id) 
        result = await session.execute(query) 
        return result.scalar() 

    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[Orders] | Orders: 
        query = select(Orders).filter_by(**filters)
        result = await session.execute(query) 
        
        if one: 
            return result.scalar() 
        return result.scalars().all() 
    
    async def update_state(self, uuid: str, state: OrdersStateEnum, session: AsyncSessionDep) -> int:
        query = (
            update(Orders)
            .where(Orders.uuid == uuid)
            .values(state=state)
            .returning(Orders.id)
        )
        result = await session.execute(query)
        return result

    async def canceled_order(self, uuid: str, session: AsyncSessionDep) -> int:
        query = (
            update(Orders)
            .where(Orders.uuid == uuid)
            .values(
                state=OrdersStateEnum.Canceled,
                delete_utc=datetime.now(timezone.utc),
            )
            .returning(Orders.id)
        )
        result = await session.execute(query)
        return result
