import json
from pydantic import ValidationError
from src.infrastructure.database.orm.db_pg_medoo import Database
from src.infrastructure.redis.redisService import RedisApi
from src.utils.datetime_utils import time_to_miliseconds
from src.api.decorators.cacheService import cache
from src.api.http.http_exceptions import http_exception_general
from src.infrastructure.redis.rateLimit import rate_limit, cache_limit


@rate_limit(max_requests=2, window=60)
async def query_rate_limit(request):
    """Esta Fucion permite Acceder al login ."""
    try:
        rd = RedisApi()
        rd.connect()
        rd.ping()
        path = request.url.path

        if rd.get_exists(path) is None:
            db = Database()
            info = db.query("select  * from demo.prueba").export("json")
            rd.set_data(path, info, time_to_miliseconds(minutes=10))
            db.close()
            return {"success": True, "data": json.loads(info), "info": {}, "code": 202}
        else:
            cache_data = rd.get_data(path)
            return {
                "success": True,
                "data": json.loads(cache_data),
                "info": {
                    "cache": True,
                },
                "code": 202,
            }

    except (ValidationError, TypeError, Exception) as e:
        print(e)
        http_exception_general("query_rate_limit ValidationError")
        


@cache_limit("demo_prueba", 1)
async def query_cache_limit():
    """Esta Fucion permite Acceder al login ."""
    try:
        print("----- demo_prueba -----------")

        db = Database()
        info = db.query("select  * from demo.prueba").export("json")
        return {"success": True, "data": json.loads(info), "info": {}, "code": 202}

    except (ValidationError, TypeError, Exception) as e:
        print(e)
        http_exception_general("query_rate_limit ValidationError")
 

def query_prueba_redis():
    """Esta Fucion permite Acceder al login ."""
    print("ingreso a query_prueba_controller")
    try:
        rd = RedisApi()
        rd.connect()
        rd.ping()

        if rd.get_exists("query_prueba") is None:
            print("save cache")
            db = Database()
            info = db.query("select  * from demo.prueba").export("json")

            print("type", type(info))
            rd.set_data("query_prueba", info, time_to_miliseconds(minutes=10))
            db.close()
            return {"success": True, "data": json.loads(info), "info": {}, "code": 304}
        else:
            print("load cache")
            cache_data = rd.get_data("query_prueba")
            return {
                "success": True,
                "data": json.loads(cache_data),
                "info": {},
                "code": 202,
            }

    except (ValidationError, TypeError, Exception) as e:
        print(e)
        http_exception_general("query_rate_limit ValidationError")


@cache(days=1)
def query_prueba_cache():
    """Esta Fucion permite Acceder al login ."""
    print("ingreso a query_prueba_controller")
    try:
        db = Database()
        print("run cache")
        info = db.query("select  * from demo.prueba").export("json")
        return {"success": True, "data": json.loads(info), "info": {}, "code": 200}

    except (ValidationError, TypeError, Exception) as e:
        print(e)
        http_exception_general("query_rate_limit ValidationError")
    finally:
        db.close()
