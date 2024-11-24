Запуск:

- docker compose up -d(в фоновом режиме). Можно запустить моментально(есть готовая конфигурация в .env)

Реализованный функционал:

- Аутентификация и авторизация(JWT). Папка - core/auth
- Получение исторических данных по конкретной валютной паре с Мосбиржи, а также за сегодняшний день. Папка - core/moex
- Отправка запросов к Gigachat API с заранее заданным промптом. Папка - core/gigachat
- Агрегирующий модуль, который сначал получает данные, а затем отдает их на анлиз ИИ. Папка - core/analyzer

Флоу программы:

- Прогон сидов для получения исторических данных за последние несколько месяцов для конкретной валюты, с последующим сохранением в бд. Файл - seeds/candles.py
- Запуск api через uvicorn. Файл - core/main.py
- Запуск celery для планирования задач, при этом задачи запускаются в конкретное время(задается в .env). Файл - core/celery_app.py
- Celery дожидается поставленного времени, и вызывает функцию, которая получает данные по символу с бирижи за сегодня, а затем
  обращаеться к бд для получения всех историчских данных и передает их в промпт к Gigachat, затем все это сохранияеться в базу

Комментарии:

- После запуска через docker compose, api будет работать на localhost:8000, документация Swagger будет находиться там же
- Специально оставил .env файл, чтобы можно было запустить сервис моментально(знаю что в продакшене это не есть хорошо)
- Для получения анализа, нужно сначала зарегистрироваться и получить токен, затем отправить запрос получение анализа
- Чтобы запустить анализ за сегодня, нужно убедиться что сегодня не выходной(Мосбиржа работает только по будням),
  в .env нужно указать переменные ANALYSIS_HOUR и ANALYSIS_MINUTE, на текущее время и презапустить docker compose

Стек:

- FastAPI
- Celery
- Docker compose
- Postgres
- Redis(как хранилище для celery)
