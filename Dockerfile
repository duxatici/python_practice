FROM python:3.14-slim

WORKDIR /app

COPY . .

RUN pip install poetry && poetry install --no-root

WORKDIR /app/src/asyncio_test
CMD ["poetry", "run", "python", "main.py"]
