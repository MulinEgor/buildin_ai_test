from fastapi import APIRouter, status, Depends

from core.auth.dependencies import get_auth_service
from core.auth.schemas.request import UserRequestSchema
from core.auth.schemas.response import TokenResponseSchema, UserResponseSchema, UserTokenResponseSchema
from core.auth.service import AuthService
from core.auth.utils.jwt import JWTHandler


router = APIRouter(
    prefix='/auth',
    tags=['Авторизация']
)


@router.post('/signup', response_model=UserTokenResponseSchema, status_code=status.HTTP_201_CREATED)
async def sign_up(
    user: UserRequestSchema,
    service: AuthService = Depends(get_auth_service)
):
    return await service.create(user)


@router.post('/login', response_model=UserTokenResponseSchema, status_code=status.HTTP_200_OK)
async def login(
    user: UserRequestSchema,
    service: AuthService = Depends(get_auth_service)
):
    return await service.get(user)


@router.get('/me', response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
async def me(
    user_uuid: str = Depends(JWTHandler.get_current_user),
    service: AuthService = Depends(get_auth_service)
):
    return await service.get_by_uuid(user_uuid)


@router.post("/refresh", response_model=TokenResponseSchema, status_code=status.HTTP_200_OK)
async def refresh(
    refresh_token: str
):
    return JWTHandler.refresh_tokens(refresh_token)
