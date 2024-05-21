"""Imports."""

from fastapi import Depends, APIRouter, Response, Request
from src.middleware.token import validate_current_token
from api.http.httpResponseService import http_response_code
from src.controller.queryController import (
    query_prueba,
    query_prueba_redis,
    query_prueba_cache,
)

from src.controller.cacheController import query_rate_limit, query_cache_limit
from src.tools.messageResponse import (
    message_response,
    message_type_error,
    message_exception_error,
)


cache = APIRouter(
    prefix="/api/v1/cache", responses={404: {"description": "Not found route"}}
)


# SEARCH GENERAL SQL
@cache.get("/demo")
async def get_cache_prueba(request: Request):
    """Route to Logear user."""
    try:
        rs = await query_rate_limit(request)

        if type(rs) is dict:
            if rs.get("success") is True:
                print(rs.get("code"))
                return http_response_code(**rs)
            else:
                return http_response_code(**rs)
        else:
            return http_response_code(
                **message_response(success=False, info={"message": "Error"}, code=500)
            )

    except TypeError as e:
        print("TypeError ---------------")
        message_type_error(e)
        message_exception_error(e, "query_prueba_controller TypeError")
    except Exception as e:
        message_exception_error(e, "/get_cache_prueba Exception demo")


@cache.get("/demos/redis")
async def get_cache_redis():
    """Route to Logear user."""
    try:
        rs = await query_cache_limit()

        if type(rs) is dict:
            if rs.get("success") is True:
                print(rs.get("code"))
                return http_response_code(**rs)
            else:
                return http_response_code(**rs)
        else:
            return http_response_code(
                **message_response(success=False, info={"message": "Error"}, code=500)
            )

    except TypeError as e:
        print("TypeError ---------------")
        message_type_error(e)
        message_exception_error(e, "query_prueba_controller TypeError")
    except Exception as e:
        message_exception_error(e, "/get_cache_prueba Exception demo")


@cache.get("/redis")
async def get_query_prueba_redis():
    """Route to Logear user."""
    try:
        rs = query_prueba_redis()

        if type(rs) is dict:
            if rs.get("success") is True:
                return http_response_code(**rs)
            else:
                return http_response_code(**rs)
        else:
            return http_response_code(
                **message_response(
                    success=False, info={"message": "error no data dict"}, code=500
                )
            )

    except TypeError as e:
        message_type_error(e)
    except Exception as e:
        print(e)
        message_exception_error(e, "/demo")
