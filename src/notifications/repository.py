from abc import ABC, abstractmethod

from sqlalchemy import update, select, insert

from src.db.db import AsyncSessionDep
from src.models.enums import NotificationsStateEnum
from src.models.models import Notifications


class NotificationsRepository(ABC): 
    @abstractmethod
    async def add(self, data: dict, session: AsyncSessionDep) -> int: ...

    @abstractmethod 
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[Notifications] | Notifications: ... 

    @abstractmethod 
    async def notification_checked(self, id: int, user_id: int, session: AsyncSessionDep) -> int: ...


class PersistenceNotificationsRepository(NotificationsRepository):
    async def add(self, data: dict, session: AsyncSessionDep) -> int: 
        query = insert(Notifications).values(**data).returning(Notifications.id) 
        result = await session.execute(query) 
        return result.scalar() 
    
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[Notifications] | Notifications: 
        query = select(Notifications).filter_by(**filters) 
        result = await session.execute(query) 

        if one: 
            return result.scalar() 
        return result.scalars().all() 

    async def notification_checked(self, id: int, user_id: int, session: AsyncSessionDep) -> int:
        query = (
            update(Notifications)
            .where(Notifications.user_id == user_id, Notifications.id == id)
            .values(state=NotificationsStateEnum.Read)
            .returning(Notifications.id)
        )
        result = await session.execute(query)
        return result.scalar()
