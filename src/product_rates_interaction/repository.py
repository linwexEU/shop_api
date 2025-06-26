from abc import ABC, abstractmethod

from sqlalchemy import select, insert

from src.db.db import AsyncSessionDep
from src.models.models import ProductRatesInteraction
from src.utils.repository import SQLAlchemyRepository


class ProductRatesInteractionRepository(ABC): 
    @abstractmethod
    async def add(self, data: dict, session: AsyncSessionDep) -> int: ...

    @abstractmethod
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[ProductRatesInteraction] | ProductRatesInteraction: ... 


class PersistenceProductRatesInteractionRepository(SQLAlchemyRepository):
    async def add(self, data: dict, session: AsyncSessionDep) -> int: 
        query = insert(ProductRatesInteraction).values(**data).returning(ProductRatesInteraction.id) 
        result = await session.execute(query) 
        return result.scalar() 
    
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[ProductRatesInteraction] | ProductRatesInteraction: 
        query = select(ProductRatesInteraction).filter_by(**filters) 
        result = await session.execute(query) 
        
        if one: 
            return result.scalar() 
        return result.scalars().all()
