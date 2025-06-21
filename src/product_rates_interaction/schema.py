from pydantic import BaseModel

from src.models.enums import ActEnum


class SLikedProductRateModel(BaseModel):
    act: ActEnum = ActEnum.Like
    user_id: int
    rate_id: int


class SLikedProductRateFilters(BaseModel):
    act: ActEnum | None = None
    user_id: int | None = None
    rate_id: int | None = None
