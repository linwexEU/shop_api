import logging
import uuid

from fastapi import HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.exc import SQLAlchemyError

from src.baskets.schema import SBasket
from src.order_items.schema import SOrderItemsModel
from src.orders.state import OrdersStateMachine
from src.orders.schema import SOrderResult, SOrders, SOrdersModel, SOrdersPayload, SOrdersFilters
from src.models.enums import OrdersStateEnum, OrdersStateChangerEnum, NotificationsTypeEnum
from src.auth.dependencies import CurrentUserDep
from src.utils.dependency import OrdersServiceDep, OrderItemsServiceDep, BasketsServiceDep
from src.logger import config_logger
from src.utils.exception import EmptyException
from src.worker.tasks import send_notification


logger = logging.getLogger(__name__) 

# Configure logger 
config_logger()


class OrdersFlow: 
    def __init__(
        self, 
        current_user: CurrentUserDep | None = None,
        orders_service: OrdersServiceDep | None = None, 
        order_items_service: OrderItemsServiceDep | None = None, 
        baskets_service: BasketsServiceDep | None = None
    ): 
        self.current_user = current_user 
        self.orders_service = orders_service 
        self.order_items_service = order_items_service
        self.baskets_service = baskets_service

    async def get_orders_flow(self) -> SOrdersPayload: 
        try:
            order_items = await self.get_cached_order_items() 

            # Generate data 
            data = [
                SOrders(
                    uuid=uuid, 
                    state=order_items[uuid]["state"], 
                    products=order_items[uuid]["products"],
                    total_price=order_items[uuid]["total_price"]
                ) 
                for uuid in order_items
            ]

            return SOrdersPayload(TotalCount=len(data), Data=data)
        except Exception as ex: 
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex) 
            else: 
                logger.error("Unknown error: %s" % ex) 
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    async def change_state_flow(self, uuid: str, state: OrdersStateChangerEnum) -> None:
        # Get current state 
        try:
            order = await self.orders_service.get_by_filters(
                SOrdersFilters(uuid=uuid)
            )
        except Exception as ex: 
            if isinstance(ex, SQLAlchemyError): 
                logger.error("Db error: %s" % ex) 
            else: 
                logger.error("Unknonw error: %s" % ex) 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order(Uuid={uuid}) was not found")

        order_state = OrdersStateMachine(uuid, self.orders_service, order.state)

        try: 
            match state.value: 
                case OrdersStateEnum.Delivering.value:
                    order_state.prepared()
                case OrdersStateEnum.Done.value: 
                    order_state.delivered()

                    # Send notification
                    send_notification.delay(order.user_id, NotificationsTypeEnum.OrderComplete.value)
                case OrdersStateEnum.Canceled.value: 
                    order_state.canceled()
        except Exception as ex: 
            logger.error("State machine error: %s" % ex) 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Invalid state transition from '{order.state.value}'")  
        
    async def make_order_flow(self) -> SOrderResult: 
        basket = await self.baskets_service.get_basket_with_products(self.current_user.id) 
        items = [SBasket.from_orm(item) for item in basket]

        if not items: 
            raise EmptyException
        
        try:
            # Make order
            order_id = await self.orders_service.add(
                SOrdersModel(
                    uuid=str(uuid.uuid4()),
                    total_price=self.calculate_total_count(items),
                    user_id=self.current_user.id
                )
            )

            # Dublicate items to OrderItems
            for item in items: 
                await self.order_items_service.add(
                    SOrderItemsModel(
                        order_id=order_id, 
                        product_id=item.product.id, 
                        user_id=self.current_user.id, 
                        quantity=item.quantity
                    )
                )

            return SOrderResult(order_id=order_id)
        except Exception as ex: 
            if isinstance(ex, SQLAlchemyError): 
                logger.error("Db error: %s" % ex) 
            else: 
                logger.error("Unknown error: %s" % ex) 
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cache(60)
    async def get_cached_order_items(self):
        order_items = await self.order_items_service.get_full_order_items(self.current_user.id) 
            
        # Aggregate by uuid
        aggregate_items = {}
        for order_item in order_items: 
            if order_item.order.uuid not in aggregate_items:
                # Base
                aggregate_items[order_item.order.uuid] = {
                    "products": [], 
                    "state": order_item.order.state , 
                    "total_price": order_item.order.total_price
                }
        
            # Product
            aggregate_items[order_item.order.uuid]["products"].append(
                {
                    "title": order_item.product.title, 
                    "image": order_item.product.image, 
                    "price": order_item.product.price, 
                    "quantity": order_item.quantity
                }
            )

        return aggregate_items

    @staticmethod
    def calculate_total_count(data: list[SBasket]) -> float: 
        return sum([item.product.price * item.quantity for item in data])
