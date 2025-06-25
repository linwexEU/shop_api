from httpx import AsyncClient, Response

from src.users.schema import SUsersAuthResponse, SUsersRegistrationResponse


class UsersCli: 
    def url(self, postfix: str) -> str:
        prefix = "/auth" 
        return f"{prefix}{postfix}"

    async def registration_user(self, data: dict, ac: AsyncClient) -> SUsersRegistrationResponse | Response:
        url = self.url("/registration") 
        response = await ac.post(url, json=data)
        
        if response.status_code == 200:
            return SUsersRegistrationResponse(**response.json())
        return response
        
    async def auth_user(self, data: dict, ac: AsyncClient) -> SUsersAuthResponse | Response: 
        url = self.url("/")
        response = await ac.post(url, json=data) 

        if response.status_code == 200:
            return SUsersAuthResponse(**response.json())
        return response 
