from src.models.models import Notifications 
from src.utils.repository import SQLAlchemyRepository 
from sqlalchemy import update 
from src.db.db import async_session_maker
from src.models.enums import NotificationsStateEnum


class NotificationsRepository(SQLAlchemyRepository): 
    model = Notifications 

    async def notification_checked(self, id: int, user_id: int) -> int: 
        async with async_session_maker() as session: 
            query = update(self.model).where(
                self.model.user_id == user_id,
                self.model.id == id
                ).values(state=NotificationsStateEnum.Read).returning(self.model.id) 
            result = await session.execute(query) 
            await session.commit() 
            return result.scalar()
