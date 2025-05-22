"""Route Login."""

from fastapi import APIRouter, HTTPException, Depends, Form, status
from pydantic import ValidationError
from src.infrastructure.log.logService import ic
from src.domain.model.user_model import User, UserPasswordChange
from src.domain.model.request_model import RequestResponse
from src.domain.model.token_model import Token
from src.api.http.httpResponseService import http_response_code
 
 


user = APIRouter(prefix="/api/v1/user", responses={404: {"description": "Not found"}})




 
@user.get("/list", response_model=RequestResponse)
async def get_all_users() -> RequestResponse:
    """Route to get all users."""
    try:
        result_user_service = user_service.get_all_users()

        return RequestResponse(success=True, data=result_user_service, info={}, code=200)

    except (ValueError, TypeError) as e:
        ic(f"Error: {e}")
        return RequestResponse(success=False, data={}, info={}, code=500)
