from datetime import datetime, timedelta
import os
from uuid import UUID
from authlib.jose.errors import BadSignatureError
from fastapi import FastAPI, HTTPException, Request, Security, status
from jose import JWTError, jwt
from fastapi import FastAPI, HTTPException, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.auth.schemas.response import TokenResponseSchema


class JWTHandler:
    secret = os.getenv('JWT_ACCESS_SECRET')
    refresh_secret = os.getenv('JWT_REFRESH_SECRET')
    algorithm = "HS256"
    access_expire_days = int(os.getenv('JWT_ACCESS_EXPIRE_DAYS'))
    refresh_expire_days = int(os.getenv('JWT_REFRESH_EXPIRE_DAYS'))

    @staticmethod
    def create_tokens(user_uuid: UUID) -> TokenResponseSchema:
        data = {"user_uuid": str(user_uuid)}
        
        access_token = JWTHandler._create_token(
            data,
            secret_key=JWTHandler.secret,
            expires_delta=timedelta(days=JWTHandler.access_expire_days)
        )
        
        refresh_token = JWTHandler._create_token(
            data,
            secret_key=JWTHandler.refresh_secret,
            expires_delta=timedelta(days=JWTHandler.refresh_expire_days)
        )
        
        return TokenResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token
        )

    @staticmethod
    def _create_token(data: dict, secret_key: str, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        
        return jwt.encode(to_encode, secret_key, algorithm=JWTHandler.algorithm)

    @staticmethod
    def verify_access_token(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> dict:
        return JWTHandler._verify_token(credentials.credentials, JWTHandler.secret)

    @staticmethod
    def verify_refresh_token(refresh_token: str) -> dict:
        return JWTHandler._verify_token(refresh_token, JWTHandler.refresh_secret)

    @staticmethod
    def _verify_token(token: str, secret_key: str) -> dict:
        try:
            payload = jwt.decode(token, secret_key, algorithms=[JWTHandler.algorithm])
            if datetime.fromtimestamp(payload.get("exp")) < datetime.utcnow():
                raise HTTPException(status_code=401, detail="Токен истёк")
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Неверный токен")

    @staticmethod
    def refresh_tokens(refresh_token: str) -> TokenResponseSchema:
        try:
            payload = JWTHandler.verify_refresh_token(refresh_token)
            payload.pop("exp", None)
            return JWTHandler.create_tokens(payload["user_uuid"])
        except HTTPException:
            raise HTTPException(status_code=401, detail="Неверный refresh токен")
        
    @staticmethod
    def get_current_user(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> str:
        payload = JWTHandler.verify_access_token(credentials)
        return payload["user_uuid"]
        
        
    
def set_jwt_exception_handler(app: FastAPI):
    @app.exception_handler(BadSignatureError)
    async def bad_signature_exception_handler(request: Request, exc: BadSignatureError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен авторизации"
        )