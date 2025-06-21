from src.notifications.schema import SNotifications, SNotificationsFilters
from src.notifications.repository import NotificationsRepository 


class NotificationsService: 
    def __init__(self, notifications_repo: NotificationsRepository): 
        self.notifications_repo: NotificationsRepository = notifications_repo() 

    async def add(self, data: SNotifications) -> int: 
        return await self.notifications_repo.add(data.model_dump()) 
    
    async def get_all(self): 
        return await self.notifications_repo.get_all() 
    
    async def get_by_filters(self, filters: SNotificationsFilters, one: bool = True): 
        return await self.notifications_repo.get_by_filters(filters.model_dump(exclude_none=True), one)
    
    async def delete_by_id(self, entity_id: int) -> int: 
        return await self.notifications_repo.delete_by_id(entity_id)

    async def notification_checked(self, id: int, user_id: int) -> int: 
        return await self.notifications_repo.notification_checked(id, user_id)
