from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy import update, insert, select

from src.db.db import AsyncSessionDep
from src.models.models import Organizations


class OrganizationsRepository(ABC): 
    @abstractmethod
    async def add(self, data: dict, session: AsyncSessionDep) -> int: ...

    @abstractmethod 
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[Organizations] | Organizations: ... 

    @abstractmethod 
    async def add_delete_utc(self, organization_id: int, delete_utc: datetime, session: AsyncSessionDep) -> None: ...


class PersistenceOrganizationsRepository(OrganizationsRepository):
    async def add(self, data: dict, session: AsyncSessionDep) -> int:
        query = insert(Organizations).values(**data).returning(Organizations.id) 
        result = await session.execute(query) 
        return result.scalar()
    
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[Organizations] | Organizations:
        query = select(Organizations).filter_by(**filters)
        result = await session.execute(query) 

        if one: 
            return result.scalar() 
        return result.scalars().all()

    async def add_delete_utc(self, organization_id: int, delete_utc: datetime, session: AsyncSessionDep) -> None:
        query = (
            update(Organizations)
            .where(Organizations.id == organization_id)
            .values(delete_utc=delete_utc)
        )
        await session.execute(query)
