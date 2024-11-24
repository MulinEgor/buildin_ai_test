from datetime import datetime
from pydantic import BaseModel


class MoexResponseSchema(BaseModel):
    date: datetime
    price: float
    volume: float
