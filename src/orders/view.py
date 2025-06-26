from fastapi import APIRouter, status

from src.auth.dependencies import AdminUserDep, CurrentUserDep
from src.db.db import AsyncSessionDep
from src.models.enums import OrdersStateChangerEnum
from src.orders.flow import OrdersFlow
from src.orders.schema import SOrderResult, SOrdersPayload
from src.utils.dependency import (BasketsServiceDep, OrderItemsServiceDep,
                                  OrdersServiceDep)

router = APIRouter()


@router.get("/", response_model=SOrdersPayload)
async def get_orders(
    current_user: CurrentUserDep, order_items_service: OrderItemsServiceDep, session: AsyncSessionDep
) -> SOrdersPayload:
    flow = OrdersFlow(
        current_user=current_user, order_items_service=order_items_service, session=session
    )
    return await flow.get_orders_flow()


@router.post("/make-order", response_model=SOrderResult)
async def make_order(
    current_user: CurrentUserDep,
    baskets_service: BasketsServiceDep,
    orders_service: OrdersServiceDep,
    order_items_service: OrderItemsServiceDep,
    session: AsyncSessionDep
) -> SOrderResult:
    flow = OrdersFlow(
        current_user=current_user,
        baskets_service=baskets_service,
        orders_service=orders_service,
        order_items_service=order_items_service,
        session=session
    )
    return await flow.make_order_flow()


@router.patch("/{uuid}/state/{state}", status_code=status.HTTP_204_NO_CONTENT)
async def change_state(
    uuid: str,
    state: OrdersStateChangerEnum,
    admin_user: AdminUserDep,
    orders_service: OrdersServiceDep,
    session: AsyncSessionDep
) -> None:
    flow = OrdersFlow(current_user=admin_user, orders_service=orders_service, session=session)
    return await flow.change_state_flow(uuid, state)
