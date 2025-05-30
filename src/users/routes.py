# src/users/routes.py
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, status
from src.users.schemas import UserDetailsModel, UserModel, UserCreateModel, UserLoginModel
from src.users.service import UserService
from src.utils.auth import encode_token, decode_token, verify_password
from src.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from src.utils.dependency import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.database import redisClient
from src.errors.error import UserAlreadyExists, UserNotFound, InvalidCredentials, InvalidToken

REFRESH_TOKEN_EXPIRY = 2

userRouter = APIRouter()
userService = UserService()
roleChecker = RoleChecker(['admin', 'user'])

@userRouter.post('/register', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    username = user_data.username

    user_exists = await userService.user_exists(email, username, session)
    if user_exists:
        raise UserAlreadyExists()
    
    new_user = await userService.create_user(user_data, session)

    return new_user

@userRouter.post('/login')
async def login(user_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    password = user_data.password

    user = await userService.get_user_by_email(email, session)
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = encode_token(
                user_data = {
                    'email': user.email,
                    'user_uid': str(user.uid),
                    'role': user.role,
                }
            )

            refresh_token = encode_token(
                user_data = {
                    'email': user.email,
                    'user_uid': str(user.uid),
                },
                refresh = True,
                expiry = timedelta(days = REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse (
                content = {
                    "message": "Login success",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "uid": str(user.uid),
                        "is_verified": user.is_verified,
                    },
                }
            )
    raise InvalidCredentials()

@userRouter.get('/refrest_token')
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = encode_token(
            user_data = token_details['user']
        )

        return JSONResponse(
            content = {
                "access_token": new_access_token
            }
        )
    
    raise InvalidToken()

@userRouter.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await redisClient.add_jti_to_blocklist(jti)

    return JSONResponse(
        content = {
            "message": "Logged out successfully",
        },
        status_code=status.HTTP_200_OK
    )

@userRouter.get('/me', response_model=UserDetailsModel)
async def get_current_user(user = Depends(get_current_user), _: bool = Depends(roleChecker)):
    return user