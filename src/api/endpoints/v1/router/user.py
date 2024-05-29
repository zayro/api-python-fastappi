"""Route Login."""

from fastapi import APIRouter, HTTPException, Depends, Form, status
from pydantic import ValidationError
from src.infrastructure.log.logService import ic
from src.domain.model.user_model import User, UserPasswordChange
from src.domain.model.auth_model import Login
from src.domain.model.request_model import RequestResponse
from src.domain.model.token_model import Token
from src.api.http.httpResponseService import http_response_code
from src.infrastructure.database.user_repository import UserRepository
from src.application.service.auth_service import AuthService
from src.application.service.user_service import UserService


user = APIRouter(prefix="/api/v1/user", responses={404: {"description": "Not found"}})


def get_user_use_service():
    """Get User Use Cases."""
    repository = UserRepository()
    return AuthService(repository)


# Define la dependencia de UserService
def get_user_service() -> UserService:
    # Aquí usarías una fábrica para obtener una instancia de UserService
    return UserService()


@user.post("/auth")
@user.post("/login")
def auth(auth_credentials: Login, auth_service: AuthService = Depends(get_user_use_service)):
    """
    Endpoint para iniciar sesión y obtener un token de acceso si las credenciales son válidas.
    """
    token = auth_service.authenticate_and_generate_token(username=auth_credentials.username, password=auth_credentials.password)

    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    return {"access_token": token, "token_type": "Bearer"}


@user.get("/list", response_model=RequestResponse)
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    """Route to get all users."""
    try:
        result_user_service = user_service.get_all_users()

        return RequestResponse(success=True, data=result_user_service, info={}, code=200)

    except (ValueError, TypeError) as e:
        ic(f"Error: {e}")
        return RequestResponse(success=False, data={}, info={}, code=500)
