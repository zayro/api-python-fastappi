from pydantic import ValidationError
from src.infrastructure.log.logService import ic
from src.utils.bcrypt_utils import hash_password, verify_password


from src.domain.model.user_model import User, UserPasswordChange
from src.domain.model.request_model import RequestResponse 

def new_user_controller(data: User):
    """Esta Fucion permite Acceder al login ."""

    try:

        data.password = hash_password(data.password)

        # Search User        result_body_json = dict((x, y) for x, y in data)

        response_controller: dict = data.model_dump()

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



 

def get_user_controller() -> RequestResponse:
    """Esta Fucion permite Acceder al login ."""

    try:


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

        response_update_password_user: dict = (data)

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
