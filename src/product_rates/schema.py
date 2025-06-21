from pydantic import BaseModel, Field

from src.models.models import ProductRates 


class SProductRatesModel(BaseModel): 
    stars: int = Field(le=5, ge=1)
    notes: str | None = None
    user_id: int
    product_id: int 


class SProductRatesFilters(BaseModel): 
    user_id: int | None = None 
    product_id: int | None = None 


class SRates(BaseModel): 
    id: int
    stars: int
    notes: str | None = None
    user_id: int
    likes: int 
    dislikes: int

    @staticmethod 
    def to_dict(rate: ProductRates) -> dict: 
        return {
            "id": rate.id,
            "stars": rate.stars, 
            "notes": rate.notes, 
            "user_id": rate.user_id, 
            "likes": rate.likes, 
            "dislikes": rate.dislikes
        }


class SRatesModel(BaseModel): 
    stars: int
    notes: str | None = None


class SRatesModelResponse(BaseModel): 
    rate_id: int 


class SRatesResult(BaseModel): 
    TotalCount: int 
    Data: list[SRates]


class SRateLikeResponse(BaseModel): 
    rate_id: int 


class SRateDislikeResponse(SRateLikeResponse): 
    pass 
