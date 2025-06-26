from abc import ABC, abstractmethod 

from sqlalchemy import select, insert

from src.db.db import AsyncSessionDep
from src.models.models import OrganizationRates


class OrganizationRatesRepository(ABC):
    @abstractmethod
    async def add(self, data: dict, session: AsyncSessionDep) -> int: ...

    @abstractmethod 
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[OrganizationRates] | OrganizationRates: ... 


class PersistenceOrganizationRatesRepository(OrganizationRatesRepository): 
    async def add(self, data: dict, session: AsyncSessionDep) -> int: 
        query = insert(OrganizationRates).values(**data).returning(OrganizationRates.id) 
        result = await session.execute(query) 
        return result.scalar() 
    
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[OrganizationRates] | OrganizationRates:
        query = select(OrganizationRates).filter_by(**filters)
        result = await session.execute(query) 
        
        if one: 
            return result.scalar() 
        return result.scalars().all()
