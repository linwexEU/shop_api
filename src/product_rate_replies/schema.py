from pydantic import BaseModel

from src.models.models import ProductRateReplies 


class SProductRateReplies(BaseModel): 
    rate_id: int
    user_id: int 
    text: str

    @staticmethod 
    def to_dict(reply: ProductRateReplies): 
        return {
            "rate_id": reply.rate_id,
            "user_id": reply.user_id, 
            "text": reply.text
        }


class SProductRateRepliesModel(BaseModel): 
    text: str 


class SProductRateRepliesModelResponse(BaseModel): 
    reply_id: int 


class SProductRateRepliesFilters(BaseModel): 
    rate_id: int | None = None 


class SProductRateRepliesResult(BaseModel): 
    TotalCount: int 
    Data: list[SProductRateReplies]
