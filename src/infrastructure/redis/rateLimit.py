import json
from fastapi import HTTPException, status, Request
from src.infrastructure.redis.redisService import RedisApi
from src.utils.datetime_utils import time_to_miliseconds


def rate_limit(max_requests: int, window: int):
    def decorator(func: any):
        async def wrapper(request):
            key = f"rate_limit:{request.client.host}:{request.url.path}"
            print(key)
            rd = RedisApi()
            if rd.is_rate_limited(key, max_requests, window):
                raise Exception("rate limit exceeded")
            return await func(request)

        return wrapper

    return decorator


def cache_limit(name, time):
    def decorator(func: any):
        async def wrapper():
            # Llama a la función original y guarda el resultado
            rs = func()
            print("🚀 ~ name:", name)
            rd = RedisApi()
            rd.connect()
            rd.ping()
            if rd.get_exists(name) is None:
                print("🚀 ~ not get_exists:", rs)
                rd.set_data(name, rs.get("data"), time_to_miliseconds(minutes=time))
                return await func()
            else:
                print("🚀 ~ get_exists:", name)
                cache_data = rd.get_data(name)
                return await {
                    "success": True,
                    "data": json.loads(cache_data),
                    "info": {},
                    "code": 202,
                }

        return wrapper

    return decorator
