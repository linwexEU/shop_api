from pydantic import BaseModel 
from datetime import datetime
from src.models.models import Notifications
from src.models.enums import NotificationsStateEnum, NotificationsTypeEnum


class SNotifications(BaseModel): 
    type: NotificationsTypeEnum
    user_id: int 


class SNotificationsFilters(BaseModel): 
    state: NotificationsStateEnum | None = None 
    type: NotificationsTypeEnum | None = None
    user_id: int | None = None


class SNotificationsModel(BaseModel): 
    id: int
    user_id: int 
    state: NotificationsStateEnum 
    type: NotificationsTypeEnum
    create_utc: datetime 

    @staticmethod 
    def from_orm(notification: Notifications) -> "SNotificationsModel": 
        return SNotificationsModel(
            id=notification.id, 
            user_id=notification.user_id,
            state=notification.state, 
            type=notification.type,
            create_utc=notification.create_utc
        )
    

class SNotificationsPayload(BaseModel): 
    NewCount: int 
    Data: list[SNotificationsModel]


class SNotificationsReadResponse(BaseModel): 
    notification_id: int 
