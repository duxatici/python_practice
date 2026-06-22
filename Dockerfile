FROM python:3.14-slim

WORKDIR /app
COPY . .

RUN pip install poetry && poetry install --no-root

WORKDIR /app/youtube
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
