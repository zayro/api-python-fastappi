"""Imports."""

from fastapi import Depends, APIRouter
from infrastructure.log.logService import ic
from src.model.searchModel import Search
from src.middleware.token import validate_current_token
from api.http.httpResponseService import http_response_code
from src.controller.generalController import search_controller, search_controllers
from src.tools.messageResponse import (
    message_response,
    message_type_error,
    message_exception_error,
)


general = APIRouter(prefix="/api/v1/general")


# SEARCH GENERAL SQL
@general.post(
    "/find", tags=["Consulta"], dependencies=[Depends(validate_current_token)]
)
async def find(data: Search):
    """Ruta que permite consultar directamente a las tablas o Vistas en la base de datos"""
    try:
        rs = search_controller(data)

        if type(rs) is dict:
            return http_response_code(**rs)

    except TypeError as e:
        print("----- TypeError Database ----- ")
        print(str(e))
        print("-------------------- ")
        return http_response_code(
            **message_response(success=False, info={"message": str(e)}, code=500)
        )
    except Exception as e:
        print("----- Exception Database... ----- ")
        print(
            type(e).__name__,  # TypeError
            __file__,  # /tmp/example.py
            e.__traceback__.tb_lineno,  # 2
            "error database",
        )
        print("--------- ERROR STR ----------- \n ")
        print(str(e))
        print("-------------------- \n")
        return http_response_code(
            **message_response(
                success=False, info={"message": str(type(e).__name__)}, code=500
            )
        )


@general.post(
    "/search", tags=["Consulta"], dependencies=[Depends(validate_current_token)]
)
async def search(data: Search):
    """Ruta que permite consultar directamente a las tablas o Vistas en la base de datos"""
    try:

        ic(data)
        rs = search_controllers(data)

        if type(rs) is dict:
            return http_response_code(**rs)

    except (TypeError, ValueError) as e:
        ic(e)
        return http_response_code(
            **message_response(
                success=False, info={"message": str(type(e).__name__)}, code=500
            )
        )
