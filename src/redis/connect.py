import redis


def cache_redis():
    try:
        cache = redis.Redis(decode_responses=True).from_url('redis://localhost:6379')
        return cache
    except Exception as e:
        print("Error connect Redis", e)



 
