import json
from pydantic import ValidationError
from src.database.postgredb.db_pg_medoo import Database
from src.service.redisService import RedisApi
from src.service.datetimeService import time_to_miliseconds
from src.service.cacheService import cache
from src.tools.messageResponse import message_type_error, message_exception_error


def query_prueba():
    """Esta Fucion permite Acceder al login ."""
    print("ingreso a query_prueba_controller")
    try:
        db = Database()

        info = db.query("select  * from demo.prueba").export("json")

        return {"success": True, "data": json.loads(info), "info": {}, "code": 200}

    except TypeError as e:
        message_type_error(e)
        message_exception_error(e, "query_prueba_controller TypeError")
    except Exception as e:
        print(e)
        message_exception_error(e, "query_prueba_controller Exception")
        return {
            "success": False,
            "data": [],
            "info": {"error": "Error al formar Sql", "message": type(e).__name__},
        }
    except ValidationError as e:
        message_exception_error(e, "query_prueba_controller ValidationError")
        print(e.errors())
    finally:
        db.close()


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

    except TypeError as e:
        message_type_error(e)
        message_exception_error(e, "query_prueba_controller TypeError")
    except Exception as e:
        print(e)
        message_exception_error(e, "query_prueba_controller Exception")
        return {
            "success": False,
            "data": [],
            "info": {"error": "Error al formar Sql", "message": type(e).__name__},
        }
    except ValidationError as e:
        message_exception_error(e, "query_prueba_controller ValidationError")
        print(e.errors())


@cache(days=1)
def query_prueba_cache():
    """Esta Fucion permite Acceder al login ."""
    print("ingreso a query_prueba_controller")
    try:
        db = Database()
        print("run cache")
        info = db.query("select  * from demo.prueba").export("json")
        return {"success": True, "data": json.loads(info), "info": {}, "code": 200}

    except TypeError as e:
        message_type_error(e)
        message_exception_error(e, "query_prueba_controller TypeError")
    except Exception as e:
        print(e)
        message_exception_error(e, "query_prueba_controller Exception")
        return {
            "success": False,
            "data": [],
            "info": {"error": "Error al formar Sql", "message": type(e).__name__},
        }
    except ValidationError as e:
        message_exception_error(e, "query_prueba_controller ValidationError")
        print(e.errors())
    finally:
        db.close()
