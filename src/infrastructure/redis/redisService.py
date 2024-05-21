import redis
import time


class RedisApi:
    cache = None

    def get_redis(self):
        redis_pool = redis.ConnectionPool(
            host="localhost", port="6379", db=0, decode_responses=True
        )
        return redis.Redis(connection_pool=redis_pool)

    def is_rate_limited(self, key, max_requests, window):
        current = int(time.time())
        window_start = current - window
        redis_conn = self.get_redis()
        results = []
        with redis_conn.pipeline() as pipe:
            try:
                pipe.zremrangebyscore(key, 0, window_start)
                pipe.zcard(key)
                pipe.zadd(key, {current: current})
                pipe.expire(key, window)
                results = pipe.execute()
            except redis.RedisError as e:
                print(f"Error RedisError: {e}")
            except Exception as e:
                print("Error connect Redis", e)

                print("-----------------\n")
        return results[1] > max_requests

    def connect(self):
        try:
            print("Connect Redis")
            self.cache = redis.Redis(decode_responses=True).from_url(
                "redis://localhost:6379"
            )
            return self.cache
        except Exception as e:
            print("Error connect Redis", e)

    def ping(self):
        print("Connect Redis Ping", self.cache.ping())

    def set_data(self, name, data, time):
        if time is not None:
            self.cache.set(name, data, time)
        else:
            self.cache.set(name, data)

    def get_data(self, name: str):
        if self.get_exists(name) is True:
            return self.cache.get(name).decode("utf-8")
        else:
            return None

    def get_exists(self, name: str):
        exist = self.cache.exists(name)
        print("get_exists: ", exist)
        if exist == 0:
            return None
        else:
            return True
