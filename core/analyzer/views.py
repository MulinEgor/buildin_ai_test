from datetime import datetime
from fastapi import APIRouter, status, Depends

from core.analyzer.dependencies import get_analyzer_service
from core.analyzer.schemas.response import AnalyzerResponseSchema
from core.analyzer.service import AnalyzerService
from core.auth.utils.jwt import JWTHandler


router = APIRouter(
    prefix='/analyzer',
    tags=['Получение свечей с анализом']
)


@router.get('/', response_model=AnalyzerResponseSchema, status_code=status.HTTP_200_OK)
async def get_by_date(
    date: datetime,
    service: AnalyzerService = Depends(get_analyzer_service),
    _: str = Depends(JWTHandler.get_current_user) # Проверка авторизации
):
    return await service.get_by_date(date)


@router.get('/all', response_model=list[AnalyzerResponseSchema], status_code=status.HTTP_200_OK)
async def get_all(
    service: AnalyzerService = Depends(get_analyzer_service),
    _: str = Depends(JWTHandler.get_current_user) # Проверка авторизации
):
    return await service.get_all()
