from abc import ABC, abstractmethod

from sqlalchemy import select, insert

from src.db.db import AsyncSessionDep
from src.models.models import OrganizationRatesInteraction


class OrganizationRatesInteractionRepository(ABC):
    @abstractmethod
    async def add(self, data: dict, session: AsyncSessionDep) -> int: ...

    @abstractmethod 
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[OrganizationRatesInteraction] | OrganizationRatesInteraction: ...


class PersistenceOrganizationRatesInteractionRepository(OrganizationRatesInteractionRepository):
    async def add(self, data: dict, session: AsyncSessionDep) -> int: 
        query = insert(OrganizationRatesInteraction).values(**data).returning(OrganizationRatesInteraction.id) 
        result = await session.execute(query) 
        return result.scalar() 
    
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True):
        query = select(OrganizationRatesInteraction).filter_by(**filters)
        result = await session.execute(query) 

        if one: 
            return result.scalar() 
        return result.scalars().all()
