from src.models.models import OrganizationRates
from src.utils.repository import SQLAlchemyRepository


class OrganizationRatesRepository(SQLAlchemyRepository):
    model = OrganizationRates
