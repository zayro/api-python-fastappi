import redis
 
 
class RedisApi:
    cache = None

    def connect(self):
        try:
            print("Connect Redis")
            self.cache = redis.Redis(decode_responses=True).from_url('redis://localhost:6379')
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
            return self.cache.get(name).decode('utf-8')
        else:
            return None

    def get_exists(self, name: str):
        exist = self.cache.exists(name)
        print("get_exists: ", exist)
        if exist == 0:
            return None
        else:
            return True
