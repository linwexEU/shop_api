from fastapi import APIRouter

from src.auth.dependencies import CurrentUserDep
from src.db.db import AsyncSessionDep
from src.notifications.flow import NotificationsFlow
from src.notifications.schema import (SNotificationsPayload,
                                      SNotificationsReadResponse)
from src.utils.dependency import NotificationsServiceDep

router = APIRouter()


@router.get("/", response_model=SNotificationsPayload)
async def get_notifications(
    current_user: CurrentUserDep, notifications_service: NotificationsServiceDep, session: AsyncSessionDep
) -> SNotificationsPayload:
    flow = NotificationsFlow(
        current_user=current_user, notifications_service=notifications_service, session=session
    )
    return await flow.get_notifications_flow()


@router.patch("/{notification_id}", response_model=SNotificationsReadResponse)
async def mark_as_read(
    notification_id: int,
    current_user: CurrentUserDep,
    notifications_service: NotificationsServiceDep,
    session: AsyncSessionDep
) -> SNotificationsReadResponse:
    flow = NotificationsFlow(
        current_user=current_user, notifications_service=notifications_service, session=session
    )
    return await flow.mark_as_read_flow(notification_id)
