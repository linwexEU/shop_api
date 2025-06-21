from pydantic import BaseModel 
from src.models.models import Products
from src.models.enums import CategoriesEnum


class SProductsModel(BaseModel): 
    category: CategoriesEnum
    title: str
    price: float 
    image: str 
    organization_id: int


class SProducts(BaseModel):
    id: int
    organization_id: int
    category: CategoriesEnum
    title: str
    price: float
    
    @staticmethod 
    def to_dict(product: Products) -> dict:
        return {
            "id": product.id, 
            "organization_id": product.organization_id,
            "category": product.category.value, 
            "title": product.title, 
            "price": product.price
        }

class SProductsResult(BaseModel): 
    TotalCount: int 
    Data: list[SProducts]


class SProductFilters(BaseModel): 
    id: int | None = None
    category: CategoriesEnum | None = None 
    title: str | None = None 
    price: float | None = None


class SProductImage(BaseModel): 
    id: int 
    image: str


class Pagination(BaseModel): 
    offset: int = 0 
    limit: int  = 60


class SProductsSearch(Pagination): 
    title: str | None = None 
    desc_price: bool | None = None 
    asc_price: bool | None = None 
    low_price: float | None = None 
    high_price: float | None = None


class SProductAddResponse(BaseModel): 
    message: str 
