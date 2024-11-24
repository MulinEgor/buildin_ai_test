from uuid import UUID

from core.auth.schemas.request import UserHashedPasswordRequestSchema
from core.database import get_prisma_session


class AuthRepository:
    async def create(self, data: UserHashedPasswordRequestSchema):
        async with get_prisma_session() as session:
            user = await session.user.create(
                data=data.model_dump()
            )
            return user

    async def get(self, data: UserHashedPasswordRequestSchema):
        async with get_prisma_session() as session:
            user = await session.user.find_first(
                where=data.model_dump() 
            )
            return user

    async def get_by_uuid(self, uuid: UUID):
        async with get_prisma_session() as session:
            user = await session.user.find_first(
                where={"uuid": uuid}
            )
            return user

    async def delete(self, uuid: UUID) -> None:
        async with get_prisma_session() as session:
            await session.user.delete(where={"uuid": uuid})

    async def exists(self, uuid: UUID) -> bool:
        async with get_prisma_session() as session:
            return await session.user.find_first(where={"uuid": uuid}) is not None
