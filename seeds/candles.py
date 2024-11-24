import asyncio

from core.analyzer.dependencies import get_moex_service
from core.moex.service import MoexService


async def seed_candles(service: MoexService = get_moex_service()):
    """
    Добавление в БД недавинх данных по валюте(500 последних дней)
    """
    try:
        await service.get_recent_data(get_only_last_day=False, save_to_db=True)
        print('Сид для свечей прошел успешно')
    except Exception as e:
        print('Ошибка при прогонки сида для свечей', e)


if __name__ == '__main__':
    asyncio.run(seed_candles())
