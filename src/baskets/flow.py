import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from src.auth.dependencies import CurrentUserDep
from src.baskets.schema import (SBasket, SBasketDeleteResponse,
                                SBasketExcelResponse, SBasketPayload,
                                SBasketResponse, SBasketsFilters,
                                SBasketsModel)
from src.config import settings
from src.db.db import AsyncSessionDep
from src.logger import config_logger
from src.utils.dependency import (BasketsServiceDep, OrderItemsServiceDep,
                                  OrdersServiceDep)
from src.utils.exception import EmptyException
from src.worker.tasks import send_products_list

logger = logging.getLogger(__name__)

# Configure logger
config_logger()


class BasketsFlow:
    def __init__(
        self,
        baskets_service: BasketsServiceDep | None = None,
        current_user: CurrentUserDep | None = None,
        orders_service: OrdersServiceDep | None = None,
        order_items_service: OrderItemsServiceDep | None = None,
        session: AsyncSessionDep | None = None
    ):
        self.baskets_service = baskets_service
        self.current_user = current_user
        self.orders_service = orders_service
        self.order_items_service = order_items_service
        self.session = session

    async def get_products_from_basket_flow(self) -> SBasketPayload:
        try:
            basket = await self.baskets_service.get_basket_with_products(
                self.current_user.id, self.session
            )
            data = [SBasket.from_orm(item) for item in basket]
            return SBasketPayload(TotalSum=self.calculate_total_count(data), Data=data)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add_product_to_basket_flow(self, product_id: int) -> SBasketResponse:
        try:
            # Check if that item already exist in basket
            item = await self.baskets_service.get_by_filters(
                SBasketsFilters(user_id=self.current_user.id, product_id=product_id), self.session
            )

            if item is None:
                item_id = await self.baskets_service.add(
                    SBasketsModel(product_id=product_id, user_id=self.current_user.id), self.session
                )
            else:
                item_id = await self.baskets_service.increase_item_count(
                    product_id, self.current_user.id, self.session
                )

            return SBasketResponse(item_id=item_id)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product(Id={product_id}) was not found",
            )

    async def delete_product_from_basket_flow(
        self, product_id: int
    ) -> SBasketDeleteResponse:
        try:
            item = await self.baskets_service.get_by_filters(
                SBasketsFilters(user_id=self.current_user.id, product_id=product_id), self.session
            )

            if item is None:
                item_id = await self.baskets_service.delete_product(
                    product_id, self.current_user.id, self.session
                )
            else:
                item_id = await self.baskets_service.decrease_item_count(
                    product_id, self.current_user.id, self.session
                )

            return SBasketDeleteResponse(item_id=item_id)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product(Id={product_id}) was not found",
            )

    async def delete_all_product_from_basket_flow(
        self, product_id: int
    ) -> SBasketDeleteResponse:
        try:
            item_id = await self.baskets_service.delete_product(
                product_id, self.current_user.id, self.session
            )
            return SBasketDeleteResponse(item_id=item_id)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product(Id={product_id}) was not found",
            )

    async def clear_basket_flow(self) -> None:
        try:
            await self.baskets_service.clear_basket(self.current_user.id, self.session)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def send_products_list_to_email_flow(self) -> SBasketExcelResponse:
        items = await self.baskets_service.get_basket_with_products(
            self.current_user.id, self.session
        )
        products = [SBasket.to_dict(item) for item in items]

        if not products:
            raise EmptyException

        try:
            send_products_list.delay(
                self.current_user.email,
                settings.AWS_EMAIL,
                "What in your basket?",
                "Here file with your products from basket",
                products,
            )
            return SBasketExcelResponse(message="File was send to your email")
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def calculate_total_count(data: list[SBasket]) -> float:
        return sum([item.product.price * item.quantity for item in data])
