from src.models.models import OrganizationRatesInteraction 
from src.utils.repository import SQLAlchemyRepository


class OrganizationRatesInteractionRepository(SQLAlchemyRepository): 
    model = OrganizationRatesInteraction
