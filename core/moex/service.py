import asyncio
from datetime import datetime
from typing import Union
from fastapi import HTTPException, status
import requests
import xml.etree.ElementTree as et
import logging

from core.moex.constants import URL
from core.moex.schemas.response import MoexResponseSchema
from core.analyzer.repository import AnalyzerRepository


class MoexService:
    def __init__(self, repository: AnalyzerRepository) -> None:
        self.repository = repository
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def get_recent_data(
        self, 
        get_only_last_day: bool = True, 
        save_to_db: bool = False
    ) -> Union[list[MoexResponseSchema], MoexResponseSchema]:
        """
        Получить последние 500 свечей с Мосбиржи, по определенному символу, заданному в constants.py, для дальнейшего анализа с ИИ.
        """
        try:
            self.logger.info(
                f"Запрос данных с MOEX. Параметры: только последний день={get_only_last_day}, сохранить в БД={save_to_db}"
            )
            
            request_url = (URL + f"&from={datetime.now().strftime('%Y-%m-%d')}") if get_only_last_day else URL
            
            response = requests.get(request_url)
            
            if response.status_code != 200:
                self.logger.error(f"Ошибка при запросе к MOEX API. Status: {response.status_code}, Response: {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            self.logger.debug("Успешно получен ответ от MOEX API")
            root = et.fromstring(response.content)
            
            results: list[MoexResponseSchema] = []
            for row in root.findall('.//row'):
                results.append(
                    MoexResponseSchema(
                        date=datetime.strptime(row.get('begin'), '%Y-%m-%d %H:%M:%S').date(),
                        price=float(row.get('close')),
                        volume=float(row.get('volume'))
                    )
                )
            
            self.logger.info(f"Обработано {len(results)} свечей")
            
            results = results if len(results) > 1 else results[0]
            
            if not save_to_db:
                self.logger.debug("Возврат данных без сохранения в БД")
                return results
            
            if save_to_db and get_only_last_day:
                self.logger.warning("Попытка сохранить данные за последний день без анализа")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Нет функционала для сохранения данных за последний день без анализа"
                )
            
            self.logger.info("Сохранение данных в БД")
            await self.repository.create_candles(results)
            self.logger.info("Данные успешно сохранены в БД")
            
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка при получении данных с MOEX: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Ошибка при получении данных: {str(e)}"
            )
            