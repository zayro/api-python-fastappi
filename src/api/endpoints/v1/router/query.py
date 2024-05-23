"""Imports."""

from fastapi import Depends, APIRouter, Response

from src.api.http.httpResponseService import http_response_code

from src.application.controller.queryController import query_prueba, query_prueba_redis, query_prueba_cache

from starlette.requests import Request


query = APIRouter(
    prefix="/api/v1/query",
    responses={404: {"description": "Not found route"}},
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
                {
                    "success": False,
                    "code": 500,
                    "info": "Erron no controlado",
                }
            )

    except (TypeError, Exception) as e:
        print(e)


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
                {
                    "success": False,
                    "code": 500,
                    "info": "Erron no controlado",
                }
            )

    except (TypeError, Exception) as e:
        print(e)


@query.get("/cache")
async def get_query_prueba_cache(
    request: Request,
):
    """Route to Logear user."""
    try:
        if "headers" in request:

            if (
                request.headers.get(
                    "If-None-Match",
                    "",
                )
                == f'W/"gatovoladors"'
            ):
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
                {
                    "success": False,
                    "code": 500,
                    "info": "Erron no controlado",
                }
            )

    except (
        TypeError,
        Exception,
    ) as e:
        print(e)
