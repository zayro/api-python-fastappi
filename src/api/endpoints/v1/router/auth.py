"""Route Login."""

from fastapi import APIRouter, Form, status, HTTPException
from src.api.http.httpResponseService import http_response_code
from src.domain.model.auth_model import Login
from src.domain.model.token_model import Token
from src.application.controller.authController import login_controller, login_doc_controller
from src.api.http.http_json_responses import http_response_code


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
            
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error no controlado")

    except (TypeError, Exception)  as e:
        print(e)
 


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
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error no controlado")

    except (TypeError, Exception)  as e:
        print(e)