from typing import Annotated

from fastapi import Depends

from src.baskets.repository import BasketsRepository
from src.baskets.service import BasketsService
from src.categories.repository import CategoriesRepository
from src.categories.service import CategoriesService
from src.notifications.repository import NotificationsRepository
from src.notifications.service import NotificationsService
from src.order_items.repository import OrderItemsRepository
from src.order_items.service import OrderItemsService
from src.orders.repository import OrdersRepository
from src.orders.service import OrdersService
from src.organization_rates.repository import OrganizationRatesRepository
from src.organization_rates.service import OgranizationRatesService
from src.organization_rates_interaction.repository import OrganizationRatesInteractionRepository
from src.organization_rates_interaction.service import OrganizationRatesInteractrionService
from src.organizations.repository import OrganizationsRepository
from src.organizations.service import OrganizationsService
from src.product_rate_replies.repository import ProductRateRepliesRepository
from src.product_rate_replies.service import ProductRateRepliesService
from src.product_rates.repository import ProductRatesRepository
from src.product_rates.service import ProductRatesService
from src.product_rates_interaction.repository import ProductRatesInteractionRepository
from src.product_rates_interaction.service import ProductRatesInteractionService
from src.products.repository import ProductsRepository
from src.products.service import ProductsService
from src.users.repository import UsersRepository
from src.users.service import UsersService


def users_service() -> UsersService:
    return UsersService(UsersRepository)


def products_service() -> ProductsService:
    return ProductsService(ProductsRepository)


def categories_service() -> CategoriesService:
    return CategoriesService(CategoriesRepository)


def baskets_service() -> BasketsService:
    return BasketsService(BasketsRepository)


def order_items_service() -> OrderItemsService:  #
    return OrderItemsService(OrderItemsRepository)


def orders_service() -> OrdersService:
    return OrdersService(OrdersRepository)


def organization_rates_service() -> OgranizationRatesService:
    return OgranizationRatesService(OrganizationRatesRepository)


def organizations_service() -> OrganizationsService:
    return OrganizationsService(OrganizationsRepository)


def product_rates_service() -> ProductRatesService:
    return ProductRatesService(ProductRatesRepository)


def product_rate_replies_service() -> ProductRateRepliesService:
    return ProductRateRepliesService(ProductRateRepliesRepository)


def product_rates_interaction_service() -> ProductRatesInteractionService:
    return ProductRatesInteractionService(ProductRatesInteractionRepository)


def organization_rates_interaction_service() -> OrganizationRatesInteractrionService:
    return OrganizationRatesInteractrionService(OrganizationRatesInteractionRepository)


def notifications_service() -> NotificationsService:
    return NotificationsService(NotificationsRepository)


UsersServiceDep = Annotated[UsersService, Depends(users_service)]
ProductsServiceDep = Annotated[ProductsService, Depends(products_service)]
CategoriesServiceDep = Annotated[CategoriesService, Depends(categories_service)]
BasketsServiceDep = Annotated[BasketsService, Depends(baskets_service)]
OrderItemsServiceDep = Annotated[OrderItemsService, Depends(order_items_service)]
OrdersServiceDep = Annotated[OrdersService, Depends(orders_service)]
OrganizationRatesServiceDep = Annotated[ OgranizationRatesService, Depends(organization_rates_service)]
OrganizationsServiceDep = Annotated[OrganizationsService, Depends(organizations_service)]
ProductRatesServiceDep = Annotated[ProductRatesService, Depends(product_rates_service)]
ProductRateRepliesServiceDep = Annotated[ProductRateRepliesService, Depends(product_rate_replies_service)]
ProductRatesInteractionDep = Annotated[ProductRatesInteractionService, Depends(product_rates_interaction_service)]
OrganizationRatesInteractionDep = Annotated[OrganizationRatesInteractrionService, Depends(organization_rates_interaction_service)]
NotificationsServiceDep = Annotated[NotificationsService, Depends(notifications_service)]
