from src.utils.repository import SQLAlchemyRepository 
from src.models.models import ProductRatesInteraction


class ProductRatesInteractionRepository(SQLAlchemyRepository): 
    model = ProductRatesInteraction
