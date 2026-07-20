import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "params, expected",
    [
        ("", 3),
        ("?oil_id=A001", 1),
        ("?oil_id=A002", 1),
        ("?delivery_type_id=1&delivery_basis_id=B01", 3),
    ],
)
async def test_happy_path(client: AsyncClient, seed_data, params: str, expected: int):
    resp = await client.get("/v1/api/trading/results" + params)

    assert resp.status_code == 200
    assert len(resp.json()) == expected


async def test_cache_hit(client: AsyncClient, seed_data, mocker):
    from fastapi_test.repositories.trading import TradingRepository

    spy = mocker.spy(TradingRepository, "get_trading_results")

    await client.get("/v1/api/trading/results")
    await client.get("/v1/api/trading/results")

    assert spy.call_count == 1
