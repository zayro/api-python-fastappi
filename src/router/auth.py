"""Route Login."""
from fastapi import APIRouter
from src.service.httpResponseService import http_response_code
from src.model.authModel import Login
from src.controller.authController import login_controller
from src.tools.messageResponse import message_response, message_type_error, message_exception_error

auth = APIRouter(prefix="/api/v1", responses={404: {"description": "Not found"}})


@auth.post("/login")
def login(data: Login):
    """Route to Logear user."""
    try:
        rs = login_controller(data)
        print(rs)

        if type(rs) is dict:
            if rs.get('success') is True:
                print("enviado info login")
                return http_response_code(**rs)
            else:
                print("error info login")
                return http_response_code( **rs)
        else:
            return http_response_code({"success": False, "code": 500, "info": "Erron no controlado"})

    except TypeError as e:
        message_type_error(e)
    except Exception as e:
        message_exception_error(e)
