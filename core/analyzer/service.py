from datetime import datetime
from fastapi import HTTPException, status
import logging

from core.analyzer.repository import AnalyzerRepository
from core.analyzer.schemas.request import AnalyzerRequestSchema
from core.gigachat.service import GigachatService
from core.moex.schemas.response import MoexResponseSchema
from core.moex.service import MoexService

class AnalyzerService:
    """
    Агрегирующий сервис для получения свечей с Мосбиржи и анализа их с помощью ИИ(ГигаЧат).
    """
    def __init__(self, gigachat_service: GigachatService, moex_service: MoexService, analyzer_repository: AnalyzerRepository) -> None:
        self.gigachat_service = gigachat_service
        self.moex_service = moex_service
        self.analyzer_repository = analyzer_repository
        self.logger = logging.getLogger(self.__class__.__name__)
        
    async def analyze(self) -> None:
        """
        Анализ свечей.
        """
        try:
            self.logger.info("Начало анализа свечей")
            today_candle: MoexResponseSchema = await self.moex_service.get_recent_data()
            self.logger.debug(f"Получены данные текущей свечи: {today_candle}")
            
            candles: list[MoexResponseSchema] = await self.analyzer_repository.get_all_candles()
            self.logger.debug(f"Получено {len(candles)} исторических свечей")
            
            ai_analysis = self.gigachat_service.analyze_candles(today_candle, candles)
            self.logger.info("Анализ ИИ успешно выполнен")
            
            await self.analyzer_repository.create_analized_candle(AnalyzerRequestSchema(ai_analysis=ai_analysis, candle=today_candle))
            self.logger.info("Результаты анализа успешно сохранены")
            
        except Exception as e:
            self.logger.error(f"Ошибка при анализе свечей: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Ошибка при анализе: {e}')
        
    async def get_all(self):
        """
        Получение всех проанализированных свечей.
        """
        try:
            self.logger.info("Запрос на получение всех проанализированных свечей")
            analized_candles = await self.analyzer_repository.get_all_analized_candles()
            
            if not analized_candles:
                self.logger.warning("Проанализированные свечи не найдены")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Свечи с анализом не найдены')
            
            self.logger.info(f"Успешно получено {len(analized_candles)} проанализированных свечей")
            return analized_candles
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Ошибка при получении всех свечей: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_by_date(self, date: datetime):
        """
        Получение проанализированных свечей за дату.
        """
        try:
            self.logger.info(f"Запрос на получение проанализированных свечей за дату: {date}")
            analized_candles = await self.analyzer_repository.get_analized_candle_by_date(date)
            
            if not analized_candles:
                self.logger.warning(f"Проанализированные свечи за дату {date} не найдены")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Свечи с анализом за данную дату не найдены')
            
            self.logger.info(f"Успешно получены свечи за дату {date}")
            return analized_candles
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Ошибка при получении свечей по дате {date}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
