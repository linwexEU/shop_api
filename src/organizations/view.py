from fastapi import APIRouter, status

from src.auth.dependencies import CurrentUserDep, OwnerUserDep
from src.db.db import AsyncSessionDep
from src.organization_rates.schema import (SOrganizationRateAdd,
                                           SOrganizationRateAddResponse,
                                           SOrganizationRatesResponse)
from src.organizations.flow import OrganizationFlow
from src.organizations.schema import (SOrganizationAdd,
                                      SOrganizationAddResponse,
                                      SOrganizationDeleteResponse,
                                      SOrganizationResponse)
from src.utils.dependency import (OrganizationRatesInteractionDep,
                                  OrganizationRatesServiceDep,
                                  OrganizationsServiceDep, UsersServiceDep)

router = APIRouter()


@router.get("/{organization_id}", response_model=SOrganizationResponse)
async def get_organization(
    organization_id: int, org_service: OrganizationsServiceDep, session: AsyncSessionDep
) -> SOrganizationResponse:
    flow = OrganizationFlow(org_service=org_service, session=session)
    return await flow.get_organization_flow(organization_id)


@router.post(
    "/add", response_model=SOrganizationAddResponse, status_code=status.HTTP_201_CREATED
)
async def add_organization(
    data: SOrganizationAdd, org_service: OrganizationsServiceDep, owner: OwnerUserDep, session: AsyncSessionDep
) -> SOrganizationAddResponse:
    flow = OrganizationFlow(org_service=org_service, session=session)
    return await flow.add_organization_flow(data, owner)


@router.delete("/{organization_id}", response_model=SOrganizationDeleteResponse)
async def delete_organization(
    organization_id: int,
    org_service: OrganizationsServiceDep,
    users_service: UsersServiceDep,
    owner: OwnerUserDep,
    session: AsyncSessionDep
) -> SOrganizationDeleteResponse:
    flow = OrganizationFlow(org_service=org_service, users_service=users_service, session=session)
    return await flow.delete_organization_flow(organization_id, owner)


@router.get("/{organization_id}/rates", response_model=SOrganizationRatesResponse)
async def get_organization_rates(
    organization_id: int, org_rates_service: OrganizationRatesServiceDep, session: AsyncSessionDep
) -> SOrganizationRatesResponse:
    flow = OrganizationFlow(org_rates_service=org_rates_service, session=session)
    return await flow.get_organization_rates_flow(organization_id=organization_id)


@router.post(
    "/{organization_id}/rates",
    response_model=SOrganizationRateAddResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_rate_to_organization(
    organization_id: int,
    data: SOrganizationRateAdd,
    current_user: CurrentUserDep,
    users_service: UsersServiceDep,
    org_rates_iter_service: OrganizationRatesInteractionDep,
    org_rates_service: OrganizationRatesServiceDep,
    session: AsyncSessionDep
) -> SOrganizationRateAddResponse:
    flow = OrganizationFlow(
        org_rates_service=org_rates_service,
        org_rates_iter_service=org_rates_iter_service,
        users_service=users_service,
        session=session
    )
    return await flow.add_rate_to_organization_flow(organization_id, data, current_user)
