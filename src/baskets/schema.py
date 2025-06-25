from pydantic import BaseModel

from src.models.models import Baskets


class SBasketsModel(BaseModel):
    user_id: int
    product_id: int


class SBasketsFilters(BaseModel):
    user_id: int | None = None
    product_id: int | None = None


class SBasketProduct(BaseModel):
    id: int
    title: str
    image: str
    price: float


class SBasket(BaseModel):
    product: SBasketProduct
    quantity: int

    @staticmethod
    def from_orm(basket: Baskets) -> "SBasket":
        return SBasket(
            product=SBasketProduct(
                id=basket.product.id,
                title=basket.product.title,
                image=basket.product.image,
                price=basket.product.price,
            ),
            quantity=basket.quantity,
        )

    @staticmethod
    def to_dict(basket: Baskets) -> dict:
        return {
            "title": basket.product.title,
            "price": basket.product.price,
            "image": basket.product.image,
            "quantity": basket.quantity,
        }


class SBasketPayload(BaseModel):
    TotalSum: float
    Data: list[SBasket]


class SBasketResponse(BaseModel):
    item_id: int


class SBasketDeleteResponse(SBasketResponse):
    pass


class SBasketExcelResponse(BaseModel):
    message: str
