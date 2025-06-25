from httpx import Response, AsyncClient

from src.notifications.schema import SNotificationsPayload, SNotificationsReadResponse 


class NotificationsCli: 
    def url(self, postfix: str) -> str: 
        prefix = "/notifications"
        return f"{prefix}{postfix}" 

    async def get_all_notifications(self, ac: AsyncClient) -> SNotificationsPayload | Response: 
        url = self.url("/")
        response = await ac.get(url) 

        if response.status_code == 200: 
            return SNotificationsPayload(**response.json())
        return response 
    
    async def mark_as_read(self, notification_id: int, ac: AsyncClient) -> SNotificationsReadResponse | Response: 
        url = self.url(f"/{notification_id}")
        response = await ac.patch(url) 

        if response.status_code == 200: 
            return SNotificationsReadResponse(**response.json())
        return response
