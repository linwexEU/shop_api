from abc import ABC, abstractmethod

from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload

from src.db.db import AsyncSessionDep
from src.models.models import Users


class UsersRepository(ABC): 
    @abstractmethod
    async def add(self, data: dict, session: AsyncSessionDep) -> int: ...

    @abstractmethod
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> Users | list[Users]: ...

    @abstractmethod 
    async def get_or_create(self, data: dict, session: AsyncSessionDep) -> Users | int: ...

    @abstractmethod 
    async def get_organizations(self, owner_id: int, session: AsyncSessionDep) -> Users: ... 


class PersistenceUsersRepository(UsersRepository):
    async def add(self, data: dict, session: AsyncSessionDep) -> int: 
        query = insert(Users).values(**data).returning(Users.id) 
        result = await session.execute(query) 
        return result.scalar() 

    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True): 
        query = select(Users).filter_by(**filters) 
        result = await session.execute(query) 
        
        if one: 
            return result.scalar() 
        return result.scalars().all() 

    async def get_or_create(self, data: dict, session: AsyncSessionDep) -> Users | int:
        query = select(Users).where(Users.email == data["email"])

        # Get user if exists
        user = await session.execute(query) 
        resulted_user = user.scalar() 

        if resulted_user: 
            return resulted_user 
        
        # Create if not exist
        query = insert(Users).values(**data).returning(Users.id) 
        created_user = await session.execute(query) 
        return created_user.scalar()

    async def get_organizations(self, owner_id: int, session: AsyncSessionDep) -> Users: 
        query = (
            select(Users)
            .where(Users.id == owner_id)
            .options(selectinload(Users.organizations))
        )
        result = await session.execute(query)
        return result.scalar()
