from datetime import datetime

from sqlalchemy import update

from src.db.db import async_session_maker
from src.models.models import Organizations
from src.utils.repository import SQLAlchemyRepository


class OrganizationsRepository(SQLAlchemyRepository):
    model = Organizations

    async def add_delete_utc(self, organization_id: int, delete_utc: datetime):
        async with async_session_maker() as session:
            query = (
                update(self.model)
                .where(self.model.id == organization_id)
                .values(delete_utc=delete_utc)
            )
            await session.execute(query)
            await session.commit()
