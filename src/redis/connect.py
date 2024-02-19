"""
The above code defines a class called RateLimiter that initializes a connection to a Redis database.
"""

from fastapi import HTTPException, status, Request
from redis import Redis, ConnectionPool, RedisError
import time


class RateLimiter:
    def __init__(self, redis_host: str, redis_port: int):
        self.redis_pool = ConnectionPool(
            host=redis_host, port=redis_port, db=0, decode_responses=True
        )

    def get_redis(self):
        return Redis(connection_pool=self.redis_pool)

    def is_rate_limited(self, key: str, max_requests: int, window: int) -> bool:
        current = int(time.time())
        window_start = current - window
        redis_conn = self.get_redis()
        with redis_conn.pipeline() as pipe:
            try:
                pipe.zremrangebyscore(key, 0, window_start)
                pipe.zcard(key)
                pipe.zadd(key, {current: current})
                pipe.expire(key, window)
                results = pipe.execute()
            except RedisError as e:
                print(f"Error RedisError: {e}")
        return results[1] > max_requests


def rate_limit(max_requests: int, window: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            key = f"rate_limit:{request.client.host}:{request.url.path}"
            if await rate_limiter.is_rate_limited(key, max_requests, window):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests",
                )
            return await func(*args, **kwargs)

        return wrapper

    return decorator
