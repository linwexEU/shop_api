from fastapi import APIRouter, UploadFile, status
from src.product_rate_replies.schema import SProductRateRepliesModel, SProductRateRepliesModelResponse, SProductRateRepliesResult
from src.product_rates.schema import SRateDislikeResponse, SRateLikeResponse, SRatesModel, SRatesModelResponse, SRatesResult
from src.products.schema import Pagination, SProductAddResponse,  SProductImage, SProductsResult, SProductsSearch
from src.models.enums import CategoriesEnum
from src.utils.dependency import ProductsServiceDep, ProductRatesServiceDep, ProductRateRepliesServiceDep, ProductRatesInteractionDep, UsersServiceDep
from src.auth.dependencies import CurrentUserDep, OwnerUserDep
from src.products.flow import ProductsFlow


router = APIRouter() 


@router.post("/{category_type}", response_model=SProductsResult)
async def get_product(pagination: Pagination, category_type: CategoriesEnum, products_service: ProductsServiceDep) -> SProductsResult: 
    flow = ProductsFlow(products_service=products_service)
    return await flow.get_products_by_category(pagination, category_type)


@router.post("/{category_type}/search", response_model=SProductsResult)
async def get_product_by_search(search: SProductsSearch, category_type: CategoriesEnum, products_service: ProductsServiceDep) -> SProductsResult: 
    flow = ProductsFlow(products_service=products_service)
    return await flow.get_products_by_search(search, category_type)


@router.get("/{product_id}/image", response_model=SProductImage)
async def get_product_image(product_id: int, products_service: ProductsServiceDep) -> SProductImage: 
    flow = ProductsFlow(products_service=products_service)
    return await flow.get_product_image(product_id)


@router.post("/add/{organization_id}", response_model=SProductAddResponse, status_code=status.HTTP_201_CREATED)
async def add_products(organization_id: int, excel_file: UploadFile, owner: OwnerUserDep, users_service: UsersServiceDep, products_service: ProductsServiceDep) -> SProductAddResponse: 
    flow = ProductsFlow(users_service=users_service, products_service=products_service) 
    return await flow.add_product_flow(organization_id, excel_file, owner)


@router.get("/{product_id}/rates", response_model=SRatesResult)
async def get_product_rates(product_id: int, product_rates_service: ProductRatesServiceDep) -> SRatesResult: 
    flow = ProductsFlow(product_rates_service=product_rates_service) 
    return await flow.get_product_rates_flow(product_id) 


@router.post("/{product_id}/rates", response_model=SRatesModelResponse, status_code=status.HTTP_201_CREATED)
async def add_product_rate(product_id, data: SRatesModel, current_user: CurrentUserDep, product_rates_service: ProductRatesServiceDep) -> SRatesModelResponse: 
    flow = ProductsFlow(product_rates_service=product_rates_service, current_user=current_user) 
    return await flow.add_product_rate_flow(product_id, data)


@router.patch("/rates/{rate_id}/like", response_model=SRateLikeResponse)
async def like_rate(rate_id: int, current_user: CurrentUserDep, product_rates_interaction_service: ProductRatesInteractionDep, product_rates_service: ProductRatesServiceDep) -> SRateLikeResponse: 
    flow = ProductsFlow(product_rates_interaction_service=product_rates_interaction_service, current_user=current_user, product_rates_service=product_rates_service) 
    return await flow.like_rate_flow(rate_id)


@router.patch("/rates/{rate_id}/dislike", response_model=SRateDislikeResponse)
async def dislike_rate(rate_id: int, current_user: CurrentUserDep, product_rates_interaction_service: ProductRatesInteractionDep, product_rates_service: ProductRatesServiceDep) -> SRateDislikeResponse: 
    flow = ProductsFlow(current_user=current_user, product_rates_interaction_service=product_rates_interaction_service, product_rates_service=product_rates_service) 
    return await flow.dislike_rate_flow(rate_id)


@router.get("/rates/{rate_id}/replies", response_model=SProductRateRepliesResult)
async def get_rate_replies(rate_id: int, product_rate_replies_service: ProductRateRepliesServiceDep) -> SProductRateRepliesResult: 
    flow = ProductsFlow(product_rate_replies_service=product_rate_replies_service)
    return await flow.get_product_rate_replies_flow(rate_id)


@router.post("/rates/{rate_id}/replies", response_model=SProductRateRepliesModelResponse, status_code=status.HTTP_201_CREATED)
async def add_reply_for_rate(rate_id: int, data: SProductRateRepliesModel, product_rate_replies_service: ProductRateRepliesServiceDep, current_user: CurrentUserDep) -> SProductRateRepliesModelResponse: 
    flow = ProductsFlow(product_rate_replies_service=product_rate_replies_service, current_user=current_user) 
    return await flow.add_product_rate_reply_flow(rate_id, data)
