# Символ акции, данные по которой будут получены с биржи (можете задать свой).
SYMBOL = 'SBER'

# URL для получения данных с Мосбиржи с интеравалом в один день.
URL = F'https://iss.moex.com/iss/engines/stock/markets/shares/securities/{SYMBOL}/candles.xml?iss.reverse=true&interval=24'
