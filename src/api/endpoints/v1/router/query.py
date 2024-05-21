"""Imports."""

from fastapi import Depends, APIRouter, Response
from src.middleware.token import validate_current_token
from api.http.httpResponseService import http_response_code
from src.controller.queryController import (
    query_prueba,
    query_prueba_redis,
    query_prueba_cache,
)
from src.tools.messageResponse import (
    message_response,
    message_type_error,
    message_exception_error,
)
from starlette.requests import Request
from fastapi_etag import Etag

query = APIRouter(
    prefix="/api/v1/query", responses={404: {"description": "Not found route"}}
)

# SEARCH GENERAL SQL


@query.get("/demo", tags=["Consulta"])
async def get_query_prueba():
    """Route to Logear user."""
    try:
        rs = query_prueba()

        if type(rs) is dict:
            if rs.get("success") is True:
                print(rs.get("code"))
                return http_response_code(**rs)
            else:
                return http_response_code(**rs)
        else:
            return http_response_code(
                {"success": False, "code": 500, "info": "Erron no controlado"}
            )

    except TypeError as e:
        message_type_error(e)
    except Exception as e:
        print(e)
        message_exception_error(e, "/demo")


@query.get("/redis")
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
                {"success": False, "code": 500, "info": "Erron no controlado"}
            )

    except TypeError as e:
        message_type_error(e)
    except Exception as e:
        print(e)
        message_exception_error(e, "/demo")


async def get_hello_etag(request: Request):
    print("if-none-match", request.headers.get("if-none-match"))
    print("if-match", request.headers.get("if-match"))
    return "etagfor" + "cache"


@query.get("/cache")
async def get_query_prueba_cache(request: Request):
    """Route to Logear user."""
    try:
        if "headers" in request:
            print("If-Modified-Since", request.headers.get("If-Modified-Since", ""))
            print("If-None-Match", request.headers.get("If-None-Match", ""))
            print("Expires", request.headers.get("Expires", ""))
            if request.headers.get("If-None-Match", "") == f'W/"gatovoladors"':
                print("archivo cacheado")
                return Response(status_code=304)

        rs = query_prueba_cache()

        if type(rs) is dict:
            if rs.get("success") is True:
                print(rs.get("code"))
                return http_response_code(**rs)
            else:
                return http_response_code(**rs)
        else:
            return http_response_code(
                {"success": False, "code": 500, "info": "Erron no controlado"}
            )

    except TypeError as e:
        message_type_error(e)
    except Exception as e:
        print(e)
        message_exception_error(e, "/cache")


@query.get("/cachedep", dependencies=[Depends(Etag(get_hello_etag))])
async def get_query_prueba_cache():
    """Route to Logear user."""
    try:

        rs = query_prueba_cache()

        if type(rs) is dict:
            if rs.get("success") is True:
                print(rs.get("code"))
                return http_response_code(**rs)
            else:
                return http_response_code(**rs)
        else:
            return http_response_code(
                {"success": False, "code": 500, "info": "Erron no controlado"}
            )

    except TypeError as e:
        message_type_error(e)
    except Exception as e:
        print(e)
        message_exception_error(e, "/demo")
