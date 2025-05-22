"""Imports."""

from fastapi import Depends, APIRouter, HTTPException, status
from src.infrastructure.log.logService import ic
from src.domain.model.search_model import Search
from src.api.middleware.token_middleware import validate_current_token
from src.api.http.httpResponseService import http_response_code
from src.application.controller.generalController import search_controller, search_controllers
 

general = APIRouter(prefix="/api/v1/general", responses={404: {"description": "Not found"}})


# SEARCH GENERAL SQL
@general.post(
    "/find", tags=["Consulta"], dependencies=[Depends(validate_current_token)]
)
async def find(data: Search):
    """Ruta que permite consultar directamente a las tablas o Vistas en la base de datos"""
    try:
        rs = search_controller(data)

        if isinstance(rs, dict):
            return http_response_code(**rs)
        else:
            return rs
 
 
    except (TypeError, ValueError) as e:
        ic(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Datos de entrada inválidos")   


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
     
