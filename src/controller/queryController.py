import json
from pydantic import ValidationError
from src.db.general import Database
from src.service.redisService import RedisApi
from src.service.datetimeService import time_to_seconds
from src.service.cacheService import cache
from src.tools.messageResponse import message_type_error, message_exception_error


def query_prueba_redis():
    """Esta Fucion permite Acceder al login ."""
    print("ingreso a query_prueba_controller")
    try:
        db = Database()
        rd = RedisApi()

        rd.connect()
        rd.ping()

        if rd.get_exists("query_prueba") is None:
            print("save cache")
            info = db.query("select  * from demo.prueba limit 1").export("json")
            print("type", type(info))
            rd.set_data("query_prueba", info, time_to_seconds(minutes=2))
            return {"success": True, "data": json.loads(info), "info": {}, "code": 200}
        else:
            print("load cache")
            cache_data = rd.get_data("query_prueba")
            print("type", type(cache_data))
            print("cache_data", cache_data)
            headers = {"Cache-Control": "max-age=3600"}
            return {"success": True, "data": json.loads(cache_data), "info": {}, "code": 200, "header": headers}

    except TypeError as e:
        message_type_error(e)
        message_exception_error(e, "query_prueba_controller TypeError")
    except Exception as e:
        print(e)
        message_exception_error(e, "query_prueba_controller Exception")
        return {"success": False,
                "data": [],
                "info": {
                    "error": "Error al formar Sql",
                    "message": type(e).__name__
                }
                }
    except ValidationError as e:
        message_exception_error(e, "query_prueba_controller ValidationError")
        print(e.errors())
    finally:
        db.close()


@cache(minutes=2)
def query_prueba_cache():
    """Esta Fucion permite Acceder al login ."""
    print("ingreso a query_prueba_controller")
    try:
        db = Database()
        print("run cache")
        info = db.query("select  * from demo.prueba limit 10").export("json")
        return {"success": True, "data": json.loads(info), "info": {}, "code": 200}

    except TypeError as e:
        message_type_error(e)
        message_exception_error(e, "query_prueba_controller TypeError")
    except Exception as e:
        print(e)
        message_exception_error(e, "query_prueba_controller Exception")
        return {"success": False,
                "data": [],
                "info": {
                    "error": "Error al formar Sql",
                    "message": type(e).__name__
                }
                }
    except ValidationError as e:
        message_exception_error(e, "query_prueba_controller ValidationError")
        print(e.errors())
    finally:
        db.close()
