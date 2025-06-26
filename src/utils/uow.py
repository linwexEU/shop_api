from abc import ABC, abstractmethod 
from typing import Self, Any

from src.db.db import AsyncSessionDep


class AbstractUnitOfWork(ABC): 
    session: AsyncSessionDep 

    @abstractmethod 
    async def commit(self) -> None: ... 

    @abstractmethod 
    async def rollback(self) -> None: ... 

    async def __aenter__(self) -> Self: 
        return self 
    
    async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None: 
        if exc_type is None: 
            await self.commit() 
        else: 
            await self.rollback() 


class UnitOfWork(AbstractUnitOfWork): 
    def __init__(self, session: AsyncSessionDep) -> None: 
        self.session = session 

    async def commit(self) -> None: 
        await self.session.commit() 

    async def rollback(self) -> None: 
        await self.session.rollback() 
