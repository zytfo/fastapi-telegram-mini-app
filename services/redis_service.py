# thirdparty
from redis import asyncio as aioredis


class RedisService:
    def __init__(self, pool):
        self.client = aioredis.Redis(connection_pool=pool, decode_responses=True)
