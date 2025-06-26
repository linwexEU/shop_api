from abc import abstractmethod, ABC

from sqlalchemy import select, insert

from src.db.db import AsyncSessionDep
from src.models.models import ProductRateReplies


class ProductRateRepliesRepository(ABC):
    @abstractmethod
    async def add(self, data: dict, session: AsyncSessionDep) -> int: ...

    @abstractmethod 
    async def get_by_filters(self, filtres: dict, session: AsyncSessionDep, one: bool = True) -> list[ProductRateReplies] | ProductRateReplies: ...


class PersistenceProductRateRepliesRepository(ProductRateRepliesRepository): 
    async def add(self, data: dict, session: AsyncSessionDep) -> int: 
        query = insert(ProductRateReplies).values(**data).returning(ProductRateReplies.id) 
        result = await session.execute(query) 
        return result.scalar() 
    
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[ProductRateReplies] | ProductRateReplies: 
        query = select(ProductRateReplies).filter_by(**filters) 
        result = await session.execute(query) 
        
        if one: 
            return result.scalar() 
        return result.scalars()
