from fastapi import APIRouter, status

from src.auth.dependencies import CurrentUserDep
from src.baskets.flow import BasketsFlow
from src.baskets.schema import (SBasketDeleteResponse, SBasketExcelResponse,
                                SBasketPayload, SBasketResponse)
from src.db.db import AsyncSessionDep
from src.utils.dependency import BasketsServiceDep

router = APIRouter()


@router.get("/", response_model=SBasketPayload)
async def get_products_from_basket(
    current_user: CurrentUserDep, baskets_service: BasketsServiceDep, session: AsyncSessionDep
) -> SBasketPayload:
    flow = BasketsFlow(baskets_service=baskets_service, current_user=current_user, session=session)
    return await flow.get_products_from_basket_flow()


@router.post("/add/{product_id}", response_model=SBasketResponse)
async def add_product_to_basket(
    product_id: int, current_user: CurrentUserDep, baskets_service: BasketsServiceDep, session: AsyncSessionDep
) -> SBasketResponse:
    flow = BasketsFlow(baskets_service=baskets_service, current_user=current_user, session=session)
    return await flow.add_product_to_basket_flow(product_id)


@router.delete("/delete/{product_id}", response_model=SBasketDeleteResponse)
async def delete_product_from_basket(
    product_id: int, current_user: CurrentUserDep, baskets_service: BasketsServiceDep, session: AsyncSessionDep
) -> SBasketDeleteResponse:
    flow = BasketsFlow(baskets_service=baskets_service, current_user=current_user, session=session)
    return await flow.delete_product_from_basket_flow(product_id)


@router.delete("/delete/{product_id}/all", response_model=SBasketDeleteResponse)
async def delete_all_product_from_basket(
    product_id: int, current_user: CurrentUserDep, baskets_service: BasketsServiceDep, session: AsyncSessionDep
) -> SBasketDeleteResponse:
    flow = BasketsFlow(baskets_service=baskets_service, current_user=current_user, session=session)
    return await flow.delete_all_product_from_basket_flow(product_id)


@router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
async def clear_basket(
    current_user: CurrentUserDep, baskets_service: BasketsServiceDep, session: AsyncSessionDep
) -> None:
    flow = BasketsFlow(current_user=current_user, baskets_service=baskets_service, session=session)
    return await flow.clear_basket_flow()


@router.post("/send-list", response_model=SBasketExcelResponse)
async def send_products_list_to_email(
    current_user: CurrentUserDep, baskets_service: BasketsServiceDep, session: AsyncSessionDep
) -> SBasketExcelResponse:
    flow = BasketsFlow(baskets_service=baskets_service, current_user=current_user, session=session)
    return await flow.send_products_list_to_email_flow()
