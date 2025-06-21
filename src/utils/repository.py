from sqlalchemy import delete, select, insert
from abc import abstractmethod, ABC 
from src.db.db import async_session_maker


class AbstarctRepository(ABC): 
    @abstractmethod 
    async def add(self, data: dict) -> int: 
        raise NotImplementedError 
    
    @abstractmethod 
    async def get_all(self): 
        raise NotImplementedError 
    
    @abstractmethod 
    async def get_by_filters(self, filters: dict, one: bool = True): 
        raise NotImplementedError 
    
    @abstractmethod 
    async def delete_by_id(self, entity_id: int): 
        raise NotImplementedError 
    

class SQLAlchemyRepository(AbstarctRepository): 
    model = None 

    async def add(self, data: dict) -> int: 
        async with async_session_maker() as session: 
            query = insert(self.model).values(**data).returning(self.model.id) 
            result = await session.execute(query) 
            await session.commit() 
            return result.scalar() 
        
    async def get_all(self): 
        async with async_session_maker() as session: 
            async with async_session_maker() as session: 
                query = select(self.model) 
                result = await session.execute(query) 
                return result.scalars().all() 
            
    async def get_by_filters(self, filters: dict, one: bool = True): 
        async with async_session_maker() as session: 
            query = select(self.model).filter_by(**filters) 
            result = await session.execute(query) 

            if one: 
                return result.scalar() 
            return result.scalars().all() 
        
    async def delete_by_id(self, entity_id: int) -> int: 
        async with async_session_maker() as session: 
            query = delete(self.model).where(self.model.id == entity_id).returning(self.model.id) 
            result = await session.execute(query) 
            await session.commit() 
            return result.scalar() 
