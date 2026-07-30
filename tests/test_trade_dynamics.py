import pytest
from httpx import AsyncClient


@pytest.mark.slow
@pytest.mark.parametrize(
    "params, expected",
    [
        ("", 3),
        ("?oil_id=A001", 1),
        ("?oil_id=A002", 1),
        (
            "?delivery_type_id=1&delivery_basis_id=B01&start_date=2024-01-15&end_date=2024-01-16",
            2,
        ),
    ],
)
async def test_happy_path(client: AsyncClient, seed_data, params: str, expected: int):
    resp = await client.get("/v1/api/trading/dynamics" + params)

    assert resp.status_code == 200
    assert len(resp.json()) == expected


@pytest.mark.slow
async def test_cache_hit(client: AsyncClient, seed_data, mocker):
    from fastapi_test.repositories.trading import TradingRepository

    spy = mocker.spy(TradingRepository, "get_dynamics")

    await client.get("/v1/api/trading/dynamics")
    await client.get("/v1/api/trading/dynamics")

    assert spy.call_count == 1
