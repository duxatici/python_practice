import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from testcontainers.redis import RedisContainer
from redis.asyncio import Redis


@pytest_asyncio.fixture(scope="session")
async def pg_container():
    from testcontainers.postgres import PostgresContainer

    with PostgresContainer("postgres:16") as c:
        yield c.get_connection_url()


@pytest_asyncio.fixture(scope="session")
async def apply_migrations(pg_container: str):
    from alembic.config import Config
    from alembic import command

    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", pg_container)
    command.upgrade(config, "head")
    yield
    command.downgrade(config, "base")


@pytest_asyncio.fixture
async def seed_data(engine: AsyncEngine):
    from sqlalchemy import text
    from fastapi_test.models.spimex_trading_results import SpimexTradingResults
    from datetime import date, datetime

    async with AsyncSession(engine) as session:
        await session.execute(text("TRUNCATE spimex_trading_results"))

        session.add_all(
            [
                SpimexTradingResults(
                    exchange_product_id="A100",
                    exchange_product_name="Product A",
                    oil_id="A001",
                    delivery_basis_id="B01",
                    delivery_basis_name="Basis A",
                    delivery_type_id="1",
                    volume=100,
                    total=10000.00,
                    count=10,
                    date=date(2024, 1, 15),
                    created_on=datetime(2024, 1, 15, 10, 0, 0),
                ),
                SpimexTradingResults(
                    exchange_product_id="A100",
                    exchange_product_name="Product A",
                    oil_id="A002",
                    delivery_basis_id="B01",
                    delivery_basis_name="Basis A",
                    delivery_type_id="1",
                    volume=100,
                    total=10000.00,
                    count=10,
                    date=date(2024, 1, 16),
                    created_on=datetime(2024, 1, 16, 10, 0, 0),
                ),
                SpimexTradingResults(
                    exchange_product_id="A100",
                    exchange_product_name="Product A",
                    oil_id="A003",
                    delivery_basis_id="B01",
                    delivery_basis_name="Basis A",
                    delivery_type_id="1",
                    volume=100,
                    total=10000.00,
                    count=10,
                    date=date(2024, 1, 17),
                    created_on=datetime(2024, 1, 17, 10, 0, 0),
                ),
            ]
        )
        await session.commit()

    yield

    async with AsyncSession(engine) as session:
        await session.execute(text("TRUNCATE spimex_trading_results"))
        await session.commit()


@pytest_asyncio.fixture(scope="session")
async def engine(pg_container: str, apply_migrations: None):
    from sqlalchemy.ext.asyncio import create_async_engine

    async_url = pg_container.replace("+psycopg2", "+asyncpg")
    engine = create_async_engine(async_url)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def redis_container():
    with RedisContainer("redis:7") as c:
        yield c


@pytest_asyncio.fixture(scope="function")
async def redis_client(redis_container: RedisContainer):
    client = Redis(
        host="localhost",
        port=redis_container.get_exposed_port(6379),
        decode_responses=True,
    )
    yield client
    await client.flushdb()


@pytest_asyncio.fixture
async def client(engine: AsyncEngine, redis_client: Redis):
    from fastapi_test.database import get_session
    from fastapi_test.cache import get_cache, Cache
    from fastapi_test.main import app
    from httpx import AsyncClient, ASGITransport

    async def _get_session():
        async with AsyncSession(engine) as session:
            yield session

    app.dependency_overrides[get_session] = _get_session

    async def _get_cache():
        return Cache(redis_client)

    app.dependency_overrides[get_cache] = _get_cache

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c

    app.dependency_overrides.clear()
