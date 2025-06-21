from src.models.models import Categories
from src.utils.repository import SQLAlchemyRepository


class CategoriesRepository(SQLAlchemyRepository):
    model = Categories
