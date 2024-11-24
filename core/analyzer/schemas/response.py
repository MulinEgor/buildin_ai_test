from datetime import datetime
from uuid import UUID

from core.analyzer.schemas.request import AnalyzerRequestSchema


class AnalyzerResponseSchema(AnalyzerRequestSchema):
    uuid: UUID
