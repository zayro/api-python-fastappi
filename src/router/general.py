"""Imports."""
from fastapi import Depends, APIRouter
from src.model.search import Search

from src.middleware.token import validate_current_token
from src.service.serviceHttp import http_response_code
from src.controller.generalController import search_controller
from src.tools.messageResponse import message_response, message_type_error, message_exception_error


general = APIRouter(
    prefix="/api/v1/general",
    responses={404: {"description": "Not found route"}}
)

# SEARCH GENERAL SQL


@general.post("/search", dependencies=[Depends(validate_current_token)])
async def search(data: Search):
    """Route to Logear user."""
    try:
        rs = search_controller(data)

        if type(rs) is dict:
            if rs.get('success') is True:

                return http_response_code(200, message_response(**rs))
            else:
                return http_response_code(400, message_response(**rs))
        else:
            return http_response_code(500, message_response(False, {}, {"message": "error no controlado"}))

    except TypeError as e:
        message_type_error(e)
    except Exception as e:
        message_exception_error(e, "/search")

# INSERT GENERAL SQL
