import json
from fastapi import Depends
from typing import Annotated
from pydantic import ValidationError
from infrastructure.log.logService import ic
from src.model.userModel import User, UserPasswordChange
from src.model.requestModel import RequestResponse
from src.model.authModel import Login
from src.database.postgredb.connect import search_query
from src.tools.toolsBcript import checkPasswd, createPasswd
from src.database.repository.query_user import (
    auth_user,
    create_user,
    update_password_user,
)
from src.service.tokenService import write_token


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


CommonsDep = Annotated[dict, Depends(common_parameters)]


def login_controller(data: Login):
    """Esta Fucion permite Acceder al login ."""
    try:

        # Search User
        info = auth_user(data)

        # Valid if exist user
        if len(info) > 0:
            # Valid if password it's match
            if checkPasswd(data.password, info[0].get("password")):
                print("creando token")
                token = write_token(
                    {
                        "username": data.username,
                        "email": info[0].get("email"),
                        "permissions": ["admin", "user:read", "user:write"],
                    }
                )
                return {
                    "success": True,
                    "data": {
                        "token": token,
                        "username": data.username,
                        "email": info[0].get("email"),
                    },
                    "info": {},
                    "code": 200,
                }

            else:
                return {
                    "success": False,
                    "data": [],
                    "info": {"message": "not match password"},
                    "code": 401,
                }
        else:
            return {
                "success": False,
                "data": [],
                "info": {"message": "not match username"},
                "code": 401,
            }

    except Exception as e:
        ic(e)


def login_controllerD(data: Login):
    """Esta Fucion permite Acceder al login ."""
    try:

        # Search User
        info = auth_user(data)

        # Valid if exist user
        if len(info) > 0:
            # Valid if password it's match
            if checkPasswd(data.password, info[0].get("password")):
                print("creando token")
                token = write_token(
                    {
                        "username": data.username,
                        "email": info[0].get("email"),
                        "permissions": ["admin", "user:read", "user:write"],
                    }
                )
                return {
                    "success": True,
                    "data": {
                        "token": token,
                        "username": data.username,
                        "email": info[0].get("email"),
                    },
                    "info": {},
                    "code": 200,
                }

            else:
                return {
                    "success": False,
                    "data": [],
                    "info": {"message": "not match password"},
                    "code": 401,
                }
        else:
            return {
                "success": False,
                "data": [],
                "info": {"message": "not match username"},
                "code": 401,
            }

    except Exception as e:
        ic(e)


def login_doc_controller(username, password):
    """Esta Fucion permite Acceder al login ."""
    try:
        # Search User
        rs = search_query(
            query="auth.users",
            fields=["password", "email", "created_at"],
            where={"username": username},
        )

        ic(rs)

        info = json.loads(rs)

        # Valid if exist user
        if len(info) > 0:
            # Valid if password it's match
            if checkPasswd(password, info[0].get("password")):
                print("creando token")
                token = write_token(
                    {
                        "username": username,
                        "email": info[0].get("email"),
                        "permissions": ["admin", "user:read", "user:write"],
                    }
                )
                return {"token": token}

            else:
                return {
                    "success": False,
                    "data": [],
                    "info": {"message": "not match password"},
                    "code": 401,
                }
        else:
            return {
                "success": False,
                "data": [],
                "info": {"message": "not match username"},
                "code": 401,
            }

    except Exception as e:
        print("----- Exception loginController ----- ")
        print(
            type(e).__name__,
            __file__,
            e,
        )
        print(str(e))
        print("---------- ")
        return "error"


def new_user_controller(data: User) -> RequestResponse:
    """Esta Fucion permite Acceder al login ."""

    try:

        data.password = createPasswd(data.password)

        # Search User        result_body_json = dict((x, y) for x, y in data)

        response_controller: dict = create_user(data.model_dump())

        ic(response_controller)
        ic(type(response_controller))

        # Validar que data sea un diccionario
        if not isinstance(response_controller, dict):
            raise TypeError("Los datos deben ser un diccionario.")

        # Valid if exist user
        if response_controller.get("success") == True:
            request_response: RequestResponse = RequestResponse(
                success=True, info=response_controller, code=200
            )

            return request_response

        else:

            request_response: RequestResponse = RequestResponse(
                success=False, info=response_controller, code=401
            )

            return request_response
    except (ValidationError, TypeError) as e:
        ic(e)

        request_response: RequestResponse = RequestResponse(
            success=False, info={"message": "error no controlado"}, code=500
        )

        return request_response


def update_user_controller(data: UserPasswordChange) -> RequestResponse:
    """Esta Fucion permite Acceder al login ."""
    try:

        # Search User   result_body_json = dict((x, y) for x, y in data)

        response_update_password_user: dict = update_password_user(data)

        ic(response_update_password_user)
        ic(type(response_update_password_user))

        # Validar que data sea un diccionario
        if not isinstance(response_update_password_user, dict):
            raise TypeError("Los datos deben ser un diccionario.")

        response_update_password_user.update({"code": 200})

        ic(response_update_password_user)

        return response_update_password_user

    except (ValidationError, TypeError) as e:
        ic(e)

        request_response: RequestResponse = RequestResponse(
            success=False, info={"message": "error no controlado"}, code=500
        )

        return request_response
