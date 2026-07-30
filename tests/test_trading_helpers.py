from freezegun import freeze_time
import pytest

from fastapi_test.routers.trading import _build_cache_key, _ttl_until_1411


@pytest.mark.parametrize(
    "param, key",
    [
        [[("days", "12")], "days=12"],
        [
            [
                ("oil_id", "A001"),
                ("delivery_type_id", "ABC"),
                ("delivery_basis_id", "001"),
            ],
            "delivery_basis_id=001&delivery_type_id=ABC&oil_id=A001",
        ],
        [
            [
                ("delivery_type_id", "ABC"),
                ("oil_id", "A001"),
                ("delivery_basis_id", "001"),
            ],
            "delivery_basis_id=001&delivery_type_id=ABC&oil_id=A001",
        ],
    ],
)
def test_build_cache_key(param, key, mocker):
    request_mock = mocker.Mock()
    request_mock.query_params.items.return_value = param
    request_mock.method = "GET"
    request_mock.url.path = "/v1/api/trading/last-dates"

    result = _build_cache_key(request_mock)

    assert f"GET:/v1/api/trading/last-dates:{key}" == result


@freeze_time("2026-01-01 14:11:00")
def test_at_1411_():
    assert _ttl_until_1411() == 24 * 3600


@freeze_time("2026-01-01 14:10:00")
def test_before_1411():
    assert _ttl_until_1411() == 60


@freeze_time("2026-01-01 14:12:00")
def test_after_1411():
    assert _ttl_until_1411() == 24 * 3600 - 60
