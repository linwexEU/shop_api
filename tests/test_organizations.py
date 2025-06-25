from httpx import AsyncClient

from tests.clients.organizations import OrganizationsCli 


organizations_cli = OrganizationsCli()


class TestOrganization: 

    async def test_get_organization(self, customer_ac: AsyncClient): 
        organization_id = 1 

        # Check organization
        organization = await organizations_cli.get_organization(organization_id, customer_ac) 

        assert organization.business_name == "TestOrganization1" 
        assert organization.create_utc is not None 
        assert organization.delete_utc is None 
        assert organization.user_id == 2

    async def test_add_organization(self, owner_ac: AsyncClient):
        # Add organization 
        data = {
            "business_name": "LinwexCorp"
        }

        organization_id = (await organizations_cli.add_organization(data, owner_ac)).organization_id

        # Check that we added organization 
        organization = await organizations_cli.get_organization(organization_id, owner_ac) 
        assert organization.business_name == data["business_name"]

    async def test_add_organization_no_owner(self, customer_ac: AsyncClient): 
        # Add organization 
        data = {
            "business_name": "LinwexCorp"
        }

        response = await organizations_cli.add_organization(data, customer_ac)
        assert response.status_code == 403

    async def test_organization_rates(self, customer_ac: AsyncClient):
        organization_id = 1 

        # Get organization's rates 
        rates = await organizations_cli.get_organization_rates(organization_id, customer_ac) 
        assert rates.TotalCount == 0 
        assert rates.Data == [] 

        # Add rate 
        data = {
            "stars": 4, 
            "notes": "Nice delivery"
        } 
        await organizations_cli.add_rate_to_organization(organization_id, data, customer_ac)

        # Check rate 
        rates = await organizations_cli.get_organization_rates(organization_id, customer_ac) 
        assert rates.TotalCount == 1 
        assert rates.Data[0].stars == 4 
        assert rates.Data[0].notes == "Nice delivery"

        # Add rate to the same organization 
        response = await organizations_cli.add_rate_to_organization(organization_id, data, customer_ac) 
        assert response.status_code == 403 
        assert response.json()["detail"] == "You have alrady had interaction with this Organization"

    async def test_organization_rate_same_owner(self, owner_ac: AsyncClient): 
        organization_id = 2 

        # Add rate 
        data = {
            "stars": 5
        }

        response = await organizations_cli.add_rate_to_organization(organization_id, data, owner_ac) 
        assert response.status_code == 403 
        assert response.json()["detail"] == "You can't rate yourself"

    async def test_delete_organization(self, owner_ac: AsyncClient): 
        organization_id = 1 

        # Get organization 
        organization = await organizations_cli.get_organization(organization_id, owner_ac) 
        assert organization.delete_utc is None 

        # Delete organization 
        await organizations_cli.delete_organization(organization_id, owner_ac) 
        
        # Check that we delete organization 
        organization = await organizations_cli.get_organization(organization_id, owner_ac) 
        assert organization.delete_utc is not None 

        # Delete the same organization 
        response = await organizations_cli.delete_organization(organization_id, owner_ac) 
        assert response.status_code == 400 
        assert response.json()["detail"] == "Organization has already deleted"
