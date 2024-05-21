"""IMPORTS."""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.infrastructure.security.jwt_handler import JWTHandler


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/doc")


def validate_current_token(token: str = Depends(oauth2_scheme)):
    """INFO."""
    try:
        print("---------------", token)
        jwt_handler = JWTHandler()
        token = jwt_handler.verify_token(token)

    except jwt.exceptions.ExpiredSignatureError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error ExpiredSignatureError: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except jwt.exceptions.InvalidSignatureError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error InvalidSignatureError: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except jwt.exceptions.DecodeError as e:
        print("-------------------", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error DecodeError: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except jwt.exceptions.InvalidTokenError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error InvalidTokenError: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
