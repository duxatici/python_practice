import json
from typing import Any

from fastapi import Request
from redis.asyncio import Redis


def get_cache(request: Request) -> Cache:
    return Cache(request.app.state.redis)


class Cache:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def get(self, key: str) -> Any:
        data = await self._redis.get(key)
        if data:
            return json.loads(data)

        return None

    async def set(self, key: str, data: Any, ttl: int) -> None:
        await self._redis.set(key, json.dumps(data, default=str), ex=ttl)
