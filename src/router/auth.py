"""Route Login."""
from fastapi import APIRouter
from src.service.serviceHttp import http_response_code
from src.model.auth import Login
from src.controller.authController import login_controller
from src.tools.messageResponse import message_response, message_type_error, message_exception_error

auth = APIRouter(prefix="/api/v1",
                 responses={404: {"description": "Not found"}})


@auth.post("/login")
def login(data: Login):
    """Route to Logear user."""
    try:
        rs = login_controller(data)

        if type(rs) is dict:
            if rs.get('success') is True:

                return http_response_code(200, message_response(**rs))
            else:
                return http_response_code(401, message_response(**rs))
        else:
            return http_response_code(500, message_response(False, {}, {"message": "error no controlado"}))

    except TypeError as e:
        message_type_error(e)
    except Exception as e:
        message_exception_error(e)
