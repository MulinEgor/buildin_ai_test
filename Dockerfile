FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python -m prisma generate

# Добавляем права на выполнение скрипта
RUN chmod +x init.sh
