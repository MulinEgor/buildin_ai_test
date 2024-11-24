from uuid import UUID
from fastapi import status, HTTPException
import logging

from core.auth.schemas.response import UserResponseSchema, UserTokenResponseSchema
from core.auth.utils.jwt import JWTHandler
from core.auth.utils.password import hash_password
from core.auth.schemas.request import UserHashedPasswordRequestSchema, UserRequestSchema
from core.auth.respository import AuthRepository


class AuthService:
    def __init__(self, repository: AuthRepository) -> None:
        self.repository = repository
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def create(self, data: UserRequestSchema) -> UserTokenResponseSchema:
        self.logger.info(f"Попытка создания нового пользователя с email: {data.email}")
        user_data = UserHashedPasswordRequestSchema(
            email=data.email,
            hashed_password=hash_password(data.password)
        )
        
        try:
            user = await self.repository.create(user_data)
            self.logger.info(f"Пользователь успешно создан: {user.email}")
            
            token = JWTHandler.create_tokens(user.uuid)
            self.logger.debug(f"Токены созданы для пользователя: {user.uuid}")
            
            return UserTokenResponseSchema(
                uuid=user.uuid,
                email=user.email,
                **token.model_dump()
            )
        except Exception as e:
            self.logger.error(f"Ошибка при создании пользователя {data.email}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Конфликт при создании: {e}')

    async def get(self, data: UserRequestSchema) -> UserTokenResponseSchema:
        self.logger.info(f"Попытка аутентификации пользователя: {data.email}")
        user_data = UserHashedPasswordRequestSchema(
            email=data.email,
            hashed_password=hash_password(data.password)
        )
        user = await self.repository.get(user_data)
        if not user:
            self.logger.warning(f"Пользователь не найден: {data.email}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
        
        self.logger.info(f"Пользователь успешно аутентифицирован: {data.email}")
        token = JWTHandler.create_tokens(user.uuid)
        self.logger.debug(f"Токены созданы для пользователя: {user.uuid}")
        
        return UserTokenResponseSchema(
            uuid=user.uuid,
            email=user.email,
            **token.model_dump()
        )
    
    async def get_by_uuid(self, uuid: UUID) -> UserResponseSchema:
        self.logger.info(f"Запрос информации о пользователе по UUID: {uuid}")
        user = await self.repository.get_by_uuid(uuid)
        if not user:
            self.logger.warning(f"Пользователь не найден по UUID: {uuid}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
        
        self.logger.debug(f"Пользователь найден: {user.email}")
        return UserResponseSchema(
            uuid=user.uuid,
            email=user.email,
        )

    async def delete(self, uuid: UUID):
        self.logger.info(f"Попытка удаления пользователя с UUID: {uuid}")
        if not await self.repository.exists(uuid):
            self.logger.warning(f"Попытка удаления несуществующего пользователя: {uuid}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
        
        await self.repository.delete(uuid)
        self.logger.info(f"Пользователь успешно удален: {uuid}")
