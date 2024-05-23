"""Imports."""

from fastapi import Depends, APIRouter
from src.infrastructure.log.logService import ic
from src.domain.model.search_model import Search
from src.api.middleware.token_middleware import validate_current_token
from src.api.http.httpResponseService import http_response_code
from src.application.controller.generalController import search_controller, search_controllers
 

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
        print("----- Exception Database... ----- ", e)
    


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
     
