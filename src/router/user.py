"""Route Login."""

from fastapi import APIRouter
from icecream import ic
from src.model.userModel import User
from src.service.httpResponseService import http_response_code
from src.controller.userController import (
    new_user_controller,
)
from src.tools.messageResponse import (
    message_response,
    message_type_error,
    message_exception_error,
)

user = APIRouter(prefix="/api/v1/user", responses={404: {"description": "Not found"}})


@user.post("/new")
def new_user(data: User):
    """Route to Logear user."""
    try:
        print("ingreso a la ruta")
        ic(data)
        rs = new_user_controller(data)

        if type(rs) is dict:
            if rs.get("success") is True:
                print("enviado info login")
                return http_response_code(**rs)
            else:
                print("error info login")
                return http_response_code(**rs)
        else:
            return http_response_code(
                **message_response(
                    success=False, info={"message": "error no controlado"}, code=500
                )
            )

    except TypeError as e:
        message_type_error(e)
    except Exception as e:
        message_exception_error(e, "error")
