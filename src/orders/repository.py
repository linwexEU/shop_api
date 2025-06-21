from datetime import datetime, timezone

from src.models.models import Orders
from src.utils.repository import SQLAlchemyRepository 
from sqlalchemy import update 
from src.db.db import async_session_maker
from src.models.enums import OrdersStateEnum


class OrdersRepository(SQLAlchemyRepository): 
    model = Orders 

    async def update_state(self, uuid: str, state: OrdersStateEnum) -> int: 
        async with async_session_maker() as session: 
            query = update(self.model).where(self.model.uuid == uuid).values(state=state).returning(self.model.id)
            result = await session.execute(query) 
            await session.commit() 
            return result 

    async def canceled_order(self, uuid: str) -> int: 
        async with async_session_maker() as session: 
            query = update(self.model).where(self.model.uuid == uuid).values(
                state=OrdersStateEnum.Canceled, delete_utc=datetime.now(timezone.utc)
            ).returning(self.model.id) 
            result = await session.execute(query) 
            await session.commit() 
            return result 
        