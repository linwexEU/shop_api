from typing import Annotated

from fastapi import Depends

from src.baskets.repository import PersistenceBasketsRepository
from src.baskets.service import BasketsService
from src.categories.repository import PersistenceCategoriesRepository
from src.categories.service import CategoriesService
from src.notifications.repository import PersistenceNotificationsRepository
from src.notifications.service import NotificationsService
from src.order_items.repository import PersistenceOrderItemsRepository
from src.order_items.service import OrderItemsService
from src.orders.repository import PersistenceOrdersRepository
from src.orders.service import OrdersService
from src.organization_rates.repository import PersistenceOrganizationRatesRepository
from src.organization_rates.service import OgranizationRatesService
from src.organization_rates_interaction.repository import PersistenceOrganizationRatesInteractionRepository
from src.organization_rates_interaction.service import OrganizationRatesInteractrionService
from src.organizations.repository import PersistenceOrganizationsRepository
from src.organizations.service import OrganizationsService
from src.product_rate_replies.repository import PersistenceProductRateRepliesRepository
from src.product_rate_replies.service import ProductRateRepliesService
from src.product_rates.repository import PersistenceProductRatesRepository
from src.product_rates.service import ProductRatesService
from src.product_rates_interaction.repository import PersistenceProductRatesInteractionRepository
from src.product_rates_interaction.service import ProductRatesInteractionService
from src.products.repository import PersistenceProductsRepository
from src.products.service import ProductsService
from src.users.repository import PersistenceUsersRepository
from src.users.service import UsersService


def users_service() -> UsersService:
    return UsersService(PersistenceUsersRepository)


def products_service() -> ProductsService:
    return ProductsService(PersistenceProductsRepository)


def categories_service() -> CategoriesService:
    return CategoriesService(PersistenceCategoriesRepository)


def baskets_service() -> BasketsService:
    return BasketsService(PersistenceBasketsRepository)


def order_items_service() -> OrderItemsService:  #
    return OrderItemsService(PersistenceOrderItemsRepository)


def orders_service() -> OrdersService:
    return OrdersService(PersistenceOrdersRepository)


def organization_rates_service() -> OgranizationRatesService:
    return OgranizationRatesService(PersistenceOrganizationRatesRepository)


def organizations_service() -> OrganizationsService:
    return OrganizationsService(PersistenceOrganizationsRepository)


def product_rates_service() -> ProductRatesService:
    return ProductRatesService(PersistenceProductRatesRepository)


def product_rate_replies_service() -> ProductRateRepliesService:
    return ProductRateRepliesService(PersistenceProductRateRepliesRepository)


def product_rates_interaction_service() -> ProductRatesInteractionService:
    return ProductRatesInteractionService(PersistenceProductRatesInteractionRepository)


def organization_rates_interaction_service() -> OrganizationRatesInteractrionService:
    return OrganizationRatesInteractrionService(PersistenceOrganizationRatesInteractionRepository)


def notifications_service() -> NotificationsService:
    return NotificationsService(PersistenceNotificationsRepository)


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
