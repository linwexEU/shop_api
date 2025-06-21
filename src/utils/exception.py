from fastapi import HTTPException, status


class BaseException(HTTPException): 
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR 
    detail = ""
    headers = None

    def __init__(self): 
        super().__init__(status_code=self.status_code, detail=self.detail, headers=self.headers)


class InvalidEmailException(BaseException): 
    status_code = status.HTTP_400_BAD_REQUEST 
    detail = "Provided email is invalid"


class AccessAdminException(BaseException): 
    status_code = status.HTTP_403_FORBIDDEN 
    detail = "Only Admin access"


class AccessOwnerException(BaseException): 
    status_code = status.HTTP_403_FORBIDDEN 
    detail = "Only Owner access"


class InvalidAdminToken(BaseException): 
    status_code = status.HTTP_400_BAD_REQUEST 
    detail = "Invalid AdminToken"


class CredentialsException(BaseException): 
    status_code = status.HTTP_401_UNAUTHORIZED 
    detail = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}


class IncorrectEmailOrPassword(BaseException): 
    status_code = status.HTTP_401_UNAUTHORIZED 
    detail = "Incorrect username or password"
    headers = {"WWW-Authenticate": "Bearer"}


class NotYourOrganizationException(BaseException): 
    status_code= status.HTTP_403_FORBIDDEN 
    detail = "Not Your Organization"


class NotExcelFileException(BaseException): 
    status_code = status.HTTP_400_BAD_REQUEST 
    detail = "Not Excel file"


class YouCantRateYourselfException(BaseException): 
    status_code = status.HTTP_403_FORBIDDEN 
    detail = "You can't rate yourself"


class InteractionException(BaseException):
    status_code = status.HTTP_403_FORBIDDEN 
    detail = "You have alrady had interaction with this Organization"


class OrganizationDeletedException(BaseException): 
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Organization has already deleted" 


class EmptyException(BaseException): 
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Your basket is empty"


class NotificationException(BaseException): 
    status_code = status.HTTP_403_FORBIDDEN 
    detail = "Not your notification"


class ParserExpcetion(Exception): 
    pass 
