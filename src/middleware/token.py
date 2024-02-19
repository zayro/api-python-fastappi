"""IMPORTS."""
import jwt
from fastapi import Depends,  HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.service.tokenService import validate_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def validate_current_token(token: str = Depends(oauth2_scheme)):
    """INFO."""
    try:
        token = validate_token(token)

        print(token)

    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error ExpiredSignatureError: {e}",
            headers={"WWW-Authenticate": "Bearer"},) from e
    except jwt.exceptions.InvalidSignatureError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error InvalidSignatureError: {e}",
            headers={"WWW-Authenticate": "Bearer"},) from e
    except jwt.exceptions.DecodeError as e:
        print("-------------------", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error DecodeError: {e}",
            headers={"WWW-Authenticate": "Bearer"},) from e
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error InvalidTokenError: {e}",
            headers={"WWW-Authenticate": "Bearer"},) from e
