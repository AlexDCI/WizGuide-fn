# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем зависимости для PostgreSQL и другие необходимые пакеты
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Собираем статику
RUN python manage.py collectstatic --noinput

# Указываем переменную окружения для Python (чтобы избежать проблем с буферизацией вывода)
ENV PYTHONUNBUFFERED=1

# Запуск gunicorn для сервера
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 wiz_guide_fn.wsgi:application"]
