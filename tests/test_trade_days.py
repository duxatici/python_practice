import pytest
from httpx import AsyncClient


@pytest.mark.slow
@pytest.mark.parametrize(
    "days, expected",
    [("", ["2024-01-17", "2024-01-16", "2024-01-15"]), ("?days=1", ["2024-01-17"])],
)
async def test_happy_path(
    client: AsyncClient, seed_data, days: str, expected: list[str]
):
    resp = await client.get("/v1/api/trading/last-dates" + days)

    assert resp.status_code == 200
    assert resp.json() == expected


@pytest.mark.slow
async def test_invalid_days(client: AsyncClient, seed_data):
    resp = await client.get("/v1/api/trading/last-dates?days=0")

    assert resp.status_code == 422
    assert resp.json()["detail"][0]["type"] == "greater_than"


@pytest.mark.slow
async def test_cache_hit(client: AsyncClient, seed_data, mocker):
    from fastapi_test.repositories.trading import TradingRepository

    spy = mocker.spy(TradingRepository, "get_last_trading_dates")

    await client.get("/v1/api/trading/last-dates?days=1")
    await client.get("/v1/api/trading/last-dates?days=1")

    assert spy.call_count == 1
