from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Response, Request, Response

from src.config import settings
from src.auth.flow import AuthFlow
from src.users.schema import SUsersAuth, SUsersAuthResponse, SUsersRegistration, SUsersRegistrationResponse
from src.utils.dependency import UsersServiceDep


router = APIRouter() 

oauth = OAuth()
oauth_kwargs = {"client_id": settings.CLIENT_ID, "client_secret": settings.CLIENT_SECRET, "client_kwargs": {"scope": "email openid profile", "redirect_url": "http://localhost:8000/auth/google_oauth2"}} 
oauth.register(name="google", server_metadata_url="https://accounts.google.com/.well-known/openid-configuration", **oauth_kwargs)


@router.post("/", response_model=SUsersAuthResponse)
async def authenticate(response: Response, users_service: UsersServiceDep, data: SUsersAuth) -> SUsersAuthResponse: 
    flow = AuthFlow(users_service)  
    return await flow.authenticate_flow(response, data)


@router.post("/registration", response_model=SUsersRegistrationResponse)
async def registration(users_service: UsersServiceDep, data: SUsersRegistration) -> SUsersRegistrationResponse: 
    flow = AuthFlow(users_service)
    return await flow.register_flow(data)   


@router.get("/google_oauth2")
async def google_oauth(request: Request): 
    flow = AuthFlow() 
    return await flow.google_oauth_flow(request)


@router.get("/google_oauth2/callback", response_model=SUsersAuthResponse)
async def google_oauth_callback(request: Request, response: Response, users_service: UsersServiceDep) -> SUsersAuthResponse: 
    flow = AuthFlow(users_service)
    return await flow.google_oauth_callback_flow(request, response)
