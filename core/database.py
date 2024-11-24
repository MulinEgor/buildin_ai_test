from typing import AsyncGenerator
from fastapi import FastAPI
from prisma import Prisma
from contextlib import asynccontextmanager


prisma = Prisma()


async def init_prisma():
    if not prisma.is_connected():
        await prisma.connect()


@asynccontextmanager
async def get_prisma_session() -> AsyncGenerator[Prisma, None]:
    if not prisma.is_connected():
        await prisma.connect()
    try:
        yield prisma
    except Exception as e:
        print(f"Database error: {e}")
        raise
    

def set_prisma_config(app: FastAPI):
    @app.on_event("startup")
    async def startup():
        await init_prisma()


    @app.on_event("shutdown")
    async def shutdown():
        if prisma.is_connected():
            await prisma.disconnect()
