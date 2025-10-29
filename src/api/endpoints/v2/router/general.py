"""Imports."""

from fastapi import Depends, APIRouter, HTTPException, status
from src.infrastructure.log.logService import ic
from src.domain.model.search_model import Search
from src.api.middleware.token_middleware import validate_current_token
from src.api.http.httpResponseService import http_response_code
from src.application.v2.controller.generalController import search_controller


generalMb = APIRouter(prefix="/api/v2/general", responses={404: {"description": "Not found"}})


@generalMb.post("/search", tags=["Consulta"])
async def search(data: Search):
    """Ruta que permite consultar directamente a las tablas o Vistas en la base de datos"""
    try:

        ic(data)
        rs = search_controller(data)

        if type(rs) is dict:
            return http_response_code(**rs)

    except (TypeError, ValueError) as e:
        ic(e)
