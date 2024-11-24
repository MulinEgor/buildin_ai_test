from core.moex.schemas.response import MoexResponseSchema


def format_candles_for_prompt(candles: list[MoexResponseSchema]) -> str:
    return '\n'.join([f'{candle.date.strftime("%Y-%m-%d")}, {candle.price}, {candle.volume}' for candle in candles])
