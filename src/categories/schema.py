from pydantic import BaseModel

from src.models.enums import CategoriesEnum


class SCategoriesModel(BaseModel):
    type: CategoriesEnum


class SCategoriesFilters(BaseModel):
    type: CategoriesEnum | None = None
