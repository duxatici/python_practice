FROM python:3.14-slim

WORKDIR /app

COPY . .

RUN pip install poetry && poetry install --no-root

WORKDIR /app/src
CMD ["poetry", "run", "uvicorn", "fastapi_test.main:app", "--host", "0.0.0.0"]
