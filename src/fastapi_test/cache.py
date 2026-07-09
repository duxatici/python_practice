from datetime import datetime, timedelta
import json
from typing import Any

from fastapi import Request
from redis.asyncio import Redis


def _ttl_until_1411() -> int:
    now = datetime.now()
    target = now.replace(hour=14, minute=11, second=0, microsecond=0)

    if now >= target:
        target += timedelta(days=1)

    return int((target - now).total_seconds())


def _build_cache_key(request: Request) -> str:
    query = sorted(request.query_params.items())
    query_str = "&".join(f"{k}={v}" for k, v in query)

    return f"{request.method}:{request.url.path}:{query_str}"


async def get_cached(request: Request) -> Any:
    key = _build_cache_key(request)
    redis: Redis = request.app.state.redis
    data = await redis.get(key)
    if data:
        return json.loads(data)

    return None


async def set_cached(request: Request, data: Any) -> None:
    key = _build_cache_key(request)
    redis: Redis = request.app.state.redis
    ttl = _ttl_until_1411()

    await redis.set(key, json.dumps(data, default=str), ex=ttl)
