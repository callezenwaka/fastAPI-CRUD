from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.utils.auth import decode_token
from src.database import redisClient, get_session
from src.users.service import UserService
from src.database.models import User
from typing import List, Any
from src.errors.error import AccessTokenRequired, InsufficientPermission, InvalidToken, RefreshTokenRequired

userService = UserService()

class TokenBearer(HTTPBearer):
    """Access token bearer"""

    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials = await super().__call__(request)

        token = credentials.credentials
        token_data = decode_token(token)

        if not self.is_valid_token(token):
            raise InvalidToken()
        
        is_blocked = await redisClient.token_in_blocklist(token_data['jti'])
        if is_blocked:
            raise InvalidToken()

        self.verify_token_data(token_data)

        return token_data

    def is_valid_token(self, token: str) -> bool:
        token_data = decode_token(token)

        return token_data is not None
    
    def verify_token_data(self, token_data: dict):
        raise NotImplementedError("Please override this methid in the child classes")

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise AccessTokenRequired()

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise RefreshTokenRequired()

async def get_current_user(token_details: dict = Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session)):
    user_email = token_details['user']['email']
    user = await userService.get_user_by_email(user_email, session)

    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True
        raise InsufficientPermission()

