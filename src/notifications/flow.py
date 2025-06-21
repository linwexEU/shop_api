import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from src.auth.dependencies import CurrentUserDep
from src.logger import config_logger
from src.models.enums import NotificationsStateEnum
from src.notifications.schema import (SNotificationsFilters,
                                      SNotificationsModel,
                                      SNotificationsPayload,
                                      SNotificationsReadResponse)
from src.utils.dependency import NotificationsServiceDep
from src.utils.exception import NotificationException

logger = logging.getLogger(__name__)

# Configure logger
config_logger()


class NotificationsFlow:
    def __init__(
        self,
        current_user: CurrentUserDep | None = None,
        notifications_service: NotificationsServiceDep | None = None,
    ):
        self.current_user = current_user
        self.notifications_service = notifications_service

    async def get_notifications_flow(self) -> SNotificationsPayload:
        try:
            notifications = await self.notifications_service.get_by_filters(
                SNotificationsFilters(user_id=self.current_user.id), False
            )
            data = [SNotificationsModel.from_orm(item) for item in notifications]
            return SNotificationsPayload(
                NewCount=len(
                    list(filter(lambda x: x.state == NotificationsStateEnum.New, data))
                ),
                Data=data,
            )
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def mark_as_read_flow(
        self, notification_id: int
    ) -> SNotificationsReadResponse:
        # Check that it your notification
        await self.check_access(notification_id)

        try:
            notification_id_db = await self.notifications_service.notification_checked(
                notification_id, self.current_user.id
            )
            return SNotificationsReadResponse(notification_id=notification_id_db)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Notification(Id={notification_id}) was not found",
            )

    async def check_access(self, notification_id: int):
        try:
            notification = await self.notifications_service.get_by_filters(
                SNotificationsFilters(id=notification_id)
            )
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Notification(Id={notification_id}) was not found",
            )

        if notification.user_id != self.current_user.id:
            raise NotificationException
