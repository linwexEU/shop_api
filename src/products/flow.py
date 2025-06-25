import logging

from fastapi import HTTPException, UploadFile, status
from fastapi_cache.decorator import cache
from sqlalchemy.exc import SQLAlchemyError

from src.auth.dependencies import CurrentUserDep, OwnerUserDep
from src.logger import config_logger
from src.models.enums import ActEnum, CategoriesEnum
from src.product_rate_replies.schema import (SProductRateReplies,
                                             SProductRateRepliesFilters,
                                             SProductRateRepliesModel,
                                             SProductRateRepliesModelResponse,
                                             SProductRateRepliesResult)
from src.product_rates.schema import (SProductRatesFilters, SProductRatesModel,
                                      SRateDislikeResponse, SRateLikeResponse,
                                      SRates, SRatesModel, SRatesModelResponse,
                                      SRatesResult)
from src.product_rates_interaction.schema import (SLikedProductRateFilters,
                                                  SLikedProductRateModel)
from src.products.schema import (Pagination, SProductAddResponse,
                                 SProductFilters, SProductImage, SProducts,
                                 SProductsResult, SProductsSearch)
from src.utils.dependency import (ProductRateRepliesServiceDep,
                                  ProductRatesInteractionDep,
                                  ProductRatesServiceDep, ProductsServiceDep,
                                  UsersServiceDep)
from src.utils.exception import (NotExcelFileException,
                                 NotYourOrganizationException)
from src.worker.tasks import add_products_background

logger = logging.getLogger(__name__)

# Configure logger
config_logger()


class ProductsFlow:
    def __init__(
        self,
        products_service: ProductsServiceDep | None = None,
        product_rates_service: ProductRatesServiceDep | None = None,
        product_rate_replies_service: ProductRateRepliesServiceDep | None = None,
        product_rates_interaction_service: ProductRatesInteractionDep | None = None,
        users_service: UsersServiceDep | None = None,
        current_user: CurrentUserDep | OwnerUserDep | None = None,
    ):
        self.products_service = products_service
        self.product_rates_service = product_rates_service
        self.product_rate_replies_service = product_rate_replies_service
        self.product_rates_interaction_service = product_rates_interaction_service
        self.users_service = users_service
        self.current_user = current_user

    async def get_products_by_category(
        self, pagination: Pagination, category: CategoriesEnum
    ) -> SProductsResult:
        try:
            products = await self.get_cached_products(category)

            # Set paginatrion
            pagination_result = products[
                pagination.offset : pagination.offset + pagination.limit
            ]

            return SProductsResult(TotalCount=len(products), Data=pagination_result)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def get_products_by_search(
        self, search: SProductsSearch, category: CategoriesEnum
    ):
        try:
            products = await self.get_cached_products_from_search(search, category)

            # Set pagination
            pagination_result = products[search.offset : search.offset + search.limit]

            return SProductsResult(TotalCount=len(products), Data=pagination_result)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add_product_flow(
        self, organization_id: int, excel_file: UploadFile, owner: OwnerUserDep
    ) -> SProductAddResponse:
        # Check that organization belong to Owner
        organizations = await self.users_service.get_organizations(owner.id)
        organizations_id = [org.id for org in organizations.organizations]

        if organization_id not in organizations_id:
            raise NotYourOrganizationException

        # Validate filename
        if excel_file.filename.split(".")[-1] not in ["xls", "xlsx"]:
            raise NotExcelFileException

        try:
            # Add products
            excel_file = await excel_file.read()
            add_products_background.delay(organization_id, excel_file)

            return SProductAddResponse(message="Your products are adding...")
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def get_product_rates_flow(self, product_id: int) -> SRatesResult:
        try:
            rates = await self.get_cached_product_rates(product_id)
            return SRatesResult(TotalCount=len(rates), Data=rates)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add_product_rate_flow(
        self, product_id: int, data: SRatesModel
    ) -> SRatesModelResponse:
        try:
            rate_id = await self.product_rates_service.add(
                SProductRatesModel(
                    user_id=self.current_user.id,
                    product_id=product_id,
                    stars=data.stars,
                    notes=data.notes,
                )
            )
            return SRatesModelResponse(rate_id=rate_id)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def get_product_rate_replies_flow(
        self, rate_id: int
    ) -> SProductRateRepliesResult:
        try:
            replies = await self.get_cached_product_rate_replies(rate_id)
            return SProductRateRepliesResult(TotalCount=len(replies), Data=replies)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Replies for Rate(Id={rate_id}) were not found",
            )

    async def add_product_rate_reply_flow(
        self, rate_id: int, data: SProductRateRepliesModel
    ) -> SProductRateRepliesModelResponse:
        try:
            reply_id = await self.product_rate_replies_service.add(
                SProductRateReplies(
                    rate_id=rate_id, text=data.text, user_id=self.current_user.id
                )
            )
            return SProductRateRepliesModelResponse(reply_id=reply_id)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def get_product_image(self, product_id: int) -> SProductImage:
        try:
            product = await self.products_service.get_by_filters(
                SProductFilters(id=product_id)
            )
            return SProductImage(id=product_id, image=product.image)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product(Id={product_id}) not found!",
            )

    async def like_rate_flow(self, rate_id: int) -> SRateLikeResponse:
        # Check that this user didn't interact with rate
        interaction = await self.get_interaction(rate_id, ActEnum.Like)

        if interaction is not None and interaction.act == ActEnum.Like:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        # Check that user have dislike
        interaction = await self.get_interaction(rate_id, ActEnum.Dislike)
        if interaction is not None:
            await self.product_rates_service.remove_dislike_rate(rate_id)

        try:
            # Add like
            rate_id = await self.product_rates_service.like_rate(
                rate_id, self.current_user.id
            )
            if rate_id is None:
                raise SQLAlchemyError

            # Add interaction
            await self.add_interaction(rate_id, ActEnum.Like)

            return SRateLikeResponse(rate_id=rate_id)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rate(Id={rate_id}) wan't found",
            )

    async def dislike_rate_flow(self, rate_id: int) -> SRateDislikeResponse:
        # Check that this user didn't interact with rate
        interaction = await self.get_interaction(rate_id, ActEnum.Dislike)

        if interaction is not None and interaction.act == ActEnum.Dislike:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        # Check that user have like
        interaction = await self.get_interaction(rate_id, ActEnum.Like)
        if interaction is not None:
            await self.product_rates_service.remove_like_rate(rate_id)

        try:
            # Add dislike
            rate_id = await self.product_rates_service.dislike_rate(
                rate_id, self.current_user.id
            )
            if rate_id is None:
                raise SQLAlchemyError

            # Add interaction
            await self.add_interaction(rate_id, ActEnum.Dislike)

            return SRateDislikeResponse(rate_id=rate_id)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknnown error: %s" % ex)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rate(Id={rate_id}) wasn't found",
            )

    async def get_interaction(self, rate_id: int, act: ActEnum):
        interaction = await self.product_rates_interaction_service.get_by_filters(
            SLikedProductRateFilters(
                act=act, user_id=self.current_user.id, rate_id=rate_id
            )
        )
        return interaction

    async def add_interaction(self, rate_id: int, act: ActEnum) -> int:
        interaction = await self.product_rates_interaction_service.add(
            SLikedProductRateModel(
                act=act, rate_id=rate_id, user_id=self.current_user.id
            )
        )
        return interaction

    @cache(120)
    async def get_cached_products(self, category: CategoriesEnum):
        query_products = await self.products_service.get_by_filters(
            SProductFilters(category=category), False
        )
        return [SProducts.to_dict(p) for p in query_products]

    @cache(120)
    async def get_cached_products_from_search(
        self, search: SProductsSearch, category: CategoriesEnum
    ):
        query_products = await self.products_service.get_products_by_search(
            search, category
        )
        if query_products:
            return [SProducts.to_dict(p) for p in query_products]
        return []

    @cache(120)
    async def get_cached_product_rates(self, product_id: int):
        rates = await self.product_rates_service.get_by_filters(
            SProductRatesFilters(product_id=product_id), False
        )
        return [SRates.to_dict(r) for r in rates]

    @cache(120)
    async def get_cached_product_rate_replies(self, rate_id: int):
        replies = await self.product_rate_replies_service.get_by_filters(
            SProductRateRepliesFilters(rate_id=rate_id), False
        )
        return [SProductRateReplies.to_dict(r) for r in replies]
