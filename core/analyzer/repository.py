from datetime import datetime
import json
from uuid import UUID

from core.analyzer.schemas.request import AnalyzerRequestSchema
from core.analyzer.schemas.response import AnalyzerResponseSchema
from core.analyzer.utils import DateTimeEncoder
from core.database import get_prisma_session
from core.moex.schemas.response import MoexResponseSchema


class AnalyzerRepository:
    """
    Класс для работы с БД(таблица analized_candles).
    """
    async def create_analized_candle(self, data: AnalyzerRequestSchema) -> None:
        async with get_prisma_session() as session:
            await session.candle.create(
                data={
                    "date": data.candle.date,
                    "price": data.candle.price,
                    "volume": data.candle.volume
                }
            )
            candle_uuid: UUID = (await session.candle.find_first(
                where={
                    "date": data.candle.date
                }
            )).uuid
            
            await session.analizedcandle.create(
                data={
                    "ai_analysis": data.ai_analysis,
                    "candle_uuid": candle_uuid
                }
            )
        
    async def get_all_analized_candles(self) -> list[AnalyzerResponseSchema]:
        async with get_prisma_session() as session:
            analized_candles = await session.analizedcandle.find_many(
                 include={
                    "candle": True
                }
            )
            return analized_candles
        
    async def get_analized_candle_by_date(self, date: datetime) -> AnalyzerResponseSchema:
        async with get_prisma_session() as session:
            analized_candle = await session.analizedcandle.find_first(
                where={
                    "candle": {
                        "date": {
                            "gte": date.replace(hour=0, minute=0, second=0),
                            "lt": date.replace(hour=23, minute=59, second=59)
                        }
                    }
                },
                include={
                    "candle": True
                }
            )
            return analized_candle
        
    async def create_candles(self, candles: list[MoexResponseSchema]) -> None:
        async with get_prisma_session() as session:
            await session.candle.delete_many()
            await session.candle.create_many(data=[candle.model_dump() for candle in candles])

    async def get_all_candles(self) -> list[MoexResponseSchema]:
        async with get_prisma_session() as session:
            candles = await session.candle.find_many()
            return candles

