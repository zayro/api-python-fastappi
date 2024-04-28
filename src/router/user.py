"""Route Login."""

from fastapi import APIRouter, Form
from pydantic import ValidationError
from src.service.logService import ic
from src.model.userModel import User, UserPasswordChange
from src.model.authModel import Login
from src.model.requestModel import RequestResponse
from src.model.tokenModel import Token
from src.service.httpResponseService import http_response_code
from src.controller.userController import (
    new_user_controller,
    update_user_controller,
    login_controller,
    login_doc_controller,
)
from src.tools.messageResponse import (
    message_response,
    message_type_error,
    message_exception_error,
)

user = APIRouter(prefix="/api/v1/user", responses={404: {"description": "Not found"}})


@user.post("/auth")
def login(data: Login):
    """Route to Logear user."""
    try:
        rs = login_controller(data)
        ic(rs)

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


@user.post("/auth/doc")
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


@user.post("/new")
def new_user(data: User):
    """Route New user."""
    try:

        response_new_user = new_user_controller(data)

        """
        ic(response_new_user)
        ic(type(response_new_user))
        """

        # Validar que data sea un diccionario
        if not isinstance(response_new_user, RequestResponse):
            raise TypeError("Los datos deben ser un diccionario.")

        if response_new_user.success is True:
            print("enviado info login")
            return http_response_code(**response_new_user.model_dump())
        else:
            print("error info login")
            return http_response_code(**response_new_user.model_dump())

    except TypeError as e:
        message_type_error(e)
    except Exception as e:
        message_exception_error(e, "error")


@user.put("/updatePassword")
def update_password(data: UserPasswordChange) -> RequestResponse:
    """Route to Logear user."""
    try:
        rs: RequestResponse = update_user_controller(data)
        ic(type(rs))
        ic(rs)
        if type(rs) is RequestResponse:
            return http_response_code(**rs.model_dump())
        else:
            return http_response_code(
                **message_response(
                    success=False, info={"message": "error no controlado"}, code=500
                )
            )

    except (TypeError, ValidationError) as e:
        message_type_error(e)
