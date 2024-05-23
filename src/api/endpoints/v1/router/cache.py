"""Imports."""

from fastapi import  APIRouter, Request
 
from src.api.http.httpResponseService import http_response_code
from src.application.controller.queryController import ( query_prueba, query_prueba_redis, query_prueba_cache,)
from src.application.controller.cacheController import query_rate_limit, query_cache_limit
from src.api.http.http_exceptions import http_exception_general


cache = APIRouter(prefix="/api/v1/cache", responses={404: {"description": "Not found route"}})


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
            return http_exception_general("Error no controlado")

    except (TypeError, Exception) as e:
        print("TypeError ---------------", e)


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
           return http_exception_general("Error no controlado")

    except (TypeError, Exception) as e:
        print("TypeError ---------------", e)


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
            return http_exception_general("Error no controlado")
            

    except (TypeError, Exception) as e:
        print("TypeError ---------------", e)
