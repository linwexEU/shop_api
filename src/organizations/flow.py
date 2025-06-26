import logging
from datetime import datetime, timezone

from fastapi import HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.exc import SQLAlchemyError

from src.auth.dependencies import CurrentUserDep, OwnerUserDep
from src.db.db import AsyncSessionDep
from src.logger import config_logger
from src.organization_rates.schema import (SOrganizationRate,
                                           SOrganizationRateAdd,
                                           SOrganizationRateAddResponse,
                                           SOrganizationRatesFilters,
                                           SOrganizationRatesModel,
                                           SOrganizationRatesResponse)
from src.organization_rates_interaction.schema import (
    SOrganizationRatesInteractionFilters, SOrganizationRatesInteractionModel)
from src.organizations.schema import (SOrganizationAdd,
                                      SOrganizationAddResponse,
                                      SOrganizationDeleteResponse,
                                      SOrganizationResponse,
                                      SOrganizationsFilters,
                                      SOrganizationsModel)
from src.utils.dependency import (OrganizationRatesInteractionDep,
                                  OrganizationRatesServiceDep,
                                  OrganizationsServiceDep, UsersServiceDep)
from src.utils.exception import (InteractionException,
                                 NotYourOrganizationException,
                                 OrganizationDeletedException,
                                 YouCantRateYourselfException)

logger = logging.getLogger(__name__)

# Configure logger
config_logger()


class OrganizationFlow:
    def __init__(
        self,
        org_service: OrganizationsServiceDep | None = None,
        org_rates_service: OrganizationRatesServiceDep | None = None,
        users_service: UsersServiceDep | None = None,
        org_rates_iter_service: OrganizationRatesInteractionDep | None = None,
        session: AsyncSessionDep | None = None
    ):
        self.org_service = org_service
        self.org_rates_service = org_rates_service
        self.users_service = users_service
        self.org_rates_iter_service = org_rates_iter_service
        self.session = session

    async def get_organization_flow(
        self, organization_id: int
    ) -> SOrganizationResponse:
        try:
            organization = await self.get_cached_organization(organization_id)
            return SOrganizationResponse(**organization)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization(Id={organization_id}) was not found",
            )

    async def add_organization_flow(
        self, data: SOrganizationAdd, owner: OwnerUserDep
    ) -> SOrganizationAddResponse:
        try:
            organization_id = await self.org_service.add(
                SOrganizationsModel(business_name=data.business_name, user_id=owner.id), self.session
            )
            return SOrganizationAddResponse(organization_id=organization_id)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def get_organization_rates_flow(
        self, organization_id: int
    ) -> SOrganizationRatesResponse:
        try:
            rates = await self.get_cached_rates(organization_id)
            return SOrganizationRatesResponse(TotalCount=len(rates), Data=rates)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization(Id={organization_id}) was not found",
            )

    async def add_rate_to_organization_flow(
        self,
        organization_id: int,
        data: SOrganizationRateAdd,
        current_user: CurrentUserDep,
    ) -> SOrganizationRateAddResponse:
        # Check that isn't owner organization
        organizations = await self.users_service.get_organizations(current_user.id, self.session)
        organizations_id = [org.id for org in organizations.organizations]

        if organization_id in organizations_id:
            raise YouCantRateYourselfException

        # Check that user hasn't interaction before
        interaction = await self.org_rates_iter_service.get_by_filters(
            SOrganizationRatesInteractionFilters(
                organization_id=organization_id, user_id=current_user.id
            ), self.session
        )

        if interaction is not None:
            raise InteractionException

        try:
            rate_id = await self.org_rates_service.add(
                SOrganizationRatesModel(
                    stars=data.stars,
                    notes=data.notes,
                    user_id=current_user.id,
                    organization_id=organization_id,
                ), self.session
            )

            # Add interaction
            await self.org_rates_iter_service.add(
                SOrganizationRatesInteractionModel(
                    user_id=current_user.id, organization_id=organization_id
                ), self.session
            )

            return SOrganizationRateAddResponse(rate_id=rate_id)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def delete_organization_flow(
        self, organization_id: int, owner: OwnerUserDep
    ) -> SOrganizationDeleteResponse:
        # Check that it's owner's organization
        organizations = await self.users_service.get_organizations(owner.id, self.session)
        organizations_id = [org.id for org in organizations.organizations]

        if organization_id not in organizations_id:
            raise NotYourOrganizationException

        # Check if organization has already deleted
        organization = await self.org_service.get_by_filters(
            SOrganizationsFilters(id=organization_id), self.session
        )

        if organization.delete_utc is not None:
            raise OrganizationDeletedException

        try:
            await self.org_service.add_delete_utc(
                organization_id, datetime.now(timezone.utc), self.session
            )
            return SOrganizationDeleteResponse(organization_id=organization_id)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @cache(300)
    async def get_cached_organization(self, organization_id: int):
        organization = await self.org_service.get_by_filters(
            SOrganizationsFilters(id=organization_id), self.session
        )
        return SOrganizationResponse.to_dict(organization)

    @cache(120)
    async def get_cached_rates(self, organization_id: int):
        rates = await self.org_rates_service.get_by_filters(
            SOrganizationRatesFilters(organization_id=organization_id), self.session, False
        )
        return [SOrganizationRate.to_dict(r) for r in rates]
