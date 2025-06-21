from src.models.models import ProductRateReplies 
from src.utils.repository import SQLAlchemyRepository 


class ProductRateRepliesRepository(SQLAlchemyRepository): 
    model = ProductRateReplies
