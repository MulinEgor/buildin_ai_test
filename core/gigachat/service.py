import os
import uuid
import requests
import logging
from fastapi import HTTPException, status

from core.gigachat.constants import API_AUTH_URL, API_HEADERS, API_AUTH_PAYLOAD, API_REQUEST_PAYLOAD, API_REQUEST_URL, API_VERIFY, PROMPT
from core.gigachat.utils import format_candles_for_prompt
from core.moex.schemas.response import MoexResponseSchema


class GigachatService:
    def __init__(self) -> None:
        self.auth_key = os.getenv('GIGACHAT_AUTH_KEY')
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def __login(self) -> None:
        """
        Получить access_token для дальнейшего использования.
        """
        request_id = str(uuid.uuid4())
        self.logger.info(f"Попытка аутентификации в GigaChat. Request ID: {request_id}")
        
        try:
            response = requests.post(
                API_AUTH_URL, 
                headers={
                    **API_HEADERS,
                    'RqUid': request_id,
                    'Authorization': f'Basic {self.auth_key}'
                },
                data=API_AUTH_PAYLOAD,
                verify=API_VERIFY
            )
            
            if response.status_code != 200:
                self.logger.error(f"Ошибка аутентификации GigaChat. Status: {response.status_code}, Response: {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            access_token = response.json().get('access_token')
            self.access_token = access_token
            self.logger.info("Успешная аутентификация в GigaChat")
            self.logger.debug(f"Получен access token длиной {len(access_token)} символов")
            
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка при аутентификации в GigaChat: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Ошибка при аутентификации: {str(e)}"
            )
    
    def analyze_candles(self, today_candle: MoexResponseSchema, candles: list[MoexResponseSchema]) -> str:
        """
        Анализ свечей.
        """
        self.logger.info("Начало анализа свечей")
        
        if not today_candle or not candles:
            self.logger.error("Недостаточно данных для анализа")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Недостаточно данных для анализа"
            )
        
        try:
            self.__login()  # Получение access_token при каждом вызове функции
            
            formatted_prompt = PROMPT.format(
                today_candle=format_candles_for_prompt([today_candle]), 
                candles=format_candles_for_prompt(candles)
            )
            
            response = requests.post(
                API_REQUEST_URL,
                headers={
                    **API_HEADERS,
                    'Authorization': f'Bearer {self.access_token}'
                },
                json={
                    **API_REQUEST_PAYLOAD,
                    'messages': [
                        {
                            'role': 'user',
                            'content': formatted_prompt
                        }
                    ]
                },
                verify=API_VERIFY
            )
            
            if response.status_code != 200:
                self.logger.error(f"Ошибка при запросе к GigaChat API. Status: {response.status_code}, Response: {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            result = response.json()['choices'][0]['message']['content']
            self.logger.info("Анализ свечей успешно завершен")
            self.logger.debug(f"Получен ответ длиной {len(result)} символов")
            
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка при анализе свечей: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Ошибка при анализе свечей: {str(e)}"
            )

