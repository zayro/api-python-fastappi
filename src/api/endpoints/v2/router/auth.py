"""Route Login."""

from fastapi import APIRouter, Form, status, HTTPException
from src.api.http.httpResponseService import http_response_code
from src.domain.model.auth_model import Login
from src.domain.model.token_model import Token
from src.application.v2.controller.authController import login_controller


authMb = APIRouter(prefix="/api/v2", responses={404: {"description": "Not found"}})


@authMb.post("/login")
def login(data: Login):
    """Route to Logear user."""
    try:
        rs = login_controller(data)
        print(rs)

        if isinstance(rs, dict):
            if rs.get("success") is True:
                print("enviado info login")
                return http_response_code(**rs)
            else:
                print("error info login")
                return http_response_code(**rs)
        else:

            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error no se entraron datos")

    except TypeError as error:
        raise RuntimeError("A TypeError occurred while executing the Route Auth Login") from error
    except HTTPException as error:
        raise RuntimeError("An HTTPException occurred while executing the Route Auth Login") from error
    except Exception as error:
        raise RuntimeError("An error occurred while executing the Route Auth Login") from error
