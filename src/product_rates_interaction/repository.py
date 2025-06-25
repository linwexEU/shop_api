from src.models.models import ProductRatesInteraction
from src.utils.repository import SQLAlchemyRepository


class ProductRatesInteractionRepository(SQLAlchemyRepository):
    model = ProductRatesInteraction
