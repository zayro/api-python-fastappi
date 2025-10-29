import json
from pydantic import ValidationError
from src.infrastructure.database.orm.db_pg_medoo import Database
from src.infrastructure.redis.redisService import RedisApi
from src.utils.datetime_utils import time_to_miliseconds


def query_prueba():
    """Esta Fucion permite Acceder al login ."""
    print("ingreso a query_prueba_controller")
    try:
        db = Database()

        info = db.query("select  * from demo.prueba").export("json")

        db.close()

        return {"success": True, "data": json.loads(info), "info": {}, "code": 200}

    except (TypeError, ValidationError, Exception) as e:
        print(e)


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
            return {"success": True, "data": json.loads(info), "info": {}, "code": 200}
        else:
            print("load cache")
            cache_data = rd.get_data("query_prueba")
            return {
                "success": True,
                "data": json.loads(cache_data),
                "info": {},
                "code": 200,
            }

    except (TypeError, ValidationError, Exception) as e:
        print(e)


def query_prueba_cache():
    """Esta Fucion permite Acceder al login ."""
    print("ingreso a query_prueba_controller")
    try:
        db = Database()
        print("run cache")
        info = db.query("select  * from demo.prueba").export("json")
        db.close()
        return {"success": True, "data": json.loads(info), "info": {}, "code": 200}

    except (TypeError, ValidationError, Exception) as e:
        print(e)
