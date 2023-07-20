"""Imports."""
from fastapi import Depends, APIRouter
from src.middleware.token import validate_current_token
from src.service.serviceHttp import http_response_code
from src.controller.queryController import query_prueba_redis, query_prueba_cache
from src.tools.messageResponse import message_response, message_type_error, message_exception_error


query = APIRouter(
    prefix="/api/v1/query",
    responses={404: {"description": "Not found route"}}
)

# SEARCH GENERAL SQL


@query.get("/demo")
async def get_query_prueba():
    """Route to Logear user."""
    try:
        rs = query_prueba_redis()

        if type(rs) is dict:
            if rs.get('success') is True:
                print(rs.get('code'))
                return http_response_code(**rs)
            else:
                return http_response_code(**rs)
        else:
            return http_response_code({"success": False, "code": 500, "info": "Erron no controlado"})

    except TypeError as e:
        message_type_error(e)
    except Exception as e:
        print(e)
        message_exception_error(e, "/demo")

        
@query.get("/redis")
async def get_query_prueba():
    """Route to Logear user."""
    try:
        rs = query_prueba_redis()

        if type(rs) is dict:
            if rs.get('success') is True:
                print(rs.get('code'))
                return http_response_code(**rs)
            else:
                return http_response_code(**rs)
        else:
            return http_response_code({"success": False, "code": 500, "info": "Erron no controlado"})

    except TypeError as e:
        message_type_error(e)
    except Exception as e:
        print(e)
        message_exception_error(e, "/demo")


@query.get("/cache")
async def get_query_prueba_cache():
    """Route to Logear user."""
    try:
        rs = query_prueba_cache()
        print("***************")
        print(type(rs))

        print("*************", rs)

        if type(rs) is dict:
            if rs.get('success') is True:
                print(rs.get('code'))
                return http_response_code(**rs)
            else:
                return http_response_code(**rs)
        else:
            return http_response_code({"success": False, "code": 500, "info": "Erron no controlado"})

    except TypeError as e:
        message_type_error(e)
    except Exception as e:
        print(e)
        message_exception_error(e, "/demo")

