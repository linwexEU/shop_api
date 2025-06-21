from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload

from src.db.db import async_session_maker
from src.models.models import Users
from src.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = Users

    async def get_or_create(self, data: dict):
        async with async_session_maker() as session:
            # Get user if exists
            query = select(self.model).where(self.model.email == data["email"])
            user = await session.execute(query)
            resulted_user = user.scalar()

            if resulted_user:
                return resulted_user

            # Create if not exist
            query = insert(self.model).values(**data).returning(self.model.id)
            created_user = await session.execute(query)
            await session.commit()
            return created_user.scalar()

    async def get_organizations(self, owner_id: int):
        async with async_session_maker() as session:
            query = (
                select(self.model)
                .where(self.model.id == owner_id)
                .options(selectinload(self.model.organizations))
            )
            result = await session.execute(query)
            return result.scalar()
