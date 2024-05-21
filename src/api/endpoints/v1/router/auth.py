"""Route Login."""

from fastapi import APIRouter, Form
from api.http.httpResponseService import http_response_code
from src.model.authModel import Login
from src.model.tokenModel import Token
from src.controller.authController import login_controller, login_doc_controller
from src.tools.messageResponse import (
    message_response,
    message_type_error,
    message_exception_error,
)

auth = APIRouter(prefix="/api/v1", responses={404: {"description": "Not found"}})


@auth.post("/login")
def login(data: Login):
    """Route to Logear user."""
    try:
        rs = login_controller(data)
        print(rs)

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


@auth.post("/login/doc")
def login_doc(username: str = Form(), password: str = Form()) -> Token:
    """Route to Logear user."""
    try:
        rs = login_doc_controller(username, password)
        print("-----------------", rs)

        if type(rs) is dict:
            if rs.get("token"):
                print("enviado info login")
                return Token(access_token=rs.get("token"), token_type="bearer")
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
