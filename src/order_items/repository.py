from src.models.models import OrderItems 
from src.utils.repository import SQLAlchemyRepository
from sqlalchemy import select 
from sqlalchemy.orm import selectinload
from src.db.db import async_session_maker 


class OrderItemsRepository(SQLAlchemyRepository): 
    model = OrderItems

    async def get_full_order_items(self, user_id: int): 
        async with async_session_maker() as session: 
            query = select(self.model).where(self.model.user_id == user_id).options(
                selectinload(self.model.order), selectinload(self.model.product)
            )
            result = await session.execute(query) 
            return result.scalars().all() 
