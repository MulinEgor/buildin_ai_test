from pydantic import BaseModel
from core.moex.schemas.response import MoexResponseSchema


class AnalyzerRequestSchema(BaseModel):
    ai_analysis: str
    candle: MoexResponseSchema
