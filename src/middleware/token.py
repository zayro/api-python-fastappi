from fastapi import  Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.controller.controllerToken import  validate_token
import jwt




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def validate_current_token(token: str = Depends(oauth2_scheme)):
    
    try: 
         token = validate_token(token)
         
         print(token)
         
    except jwt.exceptions.DecodeError as e:
        print("-------------------", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error: {e}",
            headers={"WWW-Authenticate": "Bearer"},)
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error: {e}",
            headers={"WWW-Authenticate": "Bearer"},)     
    except jwt.exceptions.InvalidSignatureError as e:
        print (e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error: {e}",
            headers={"WWW-Authenticate": "Bearer"},)     
    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error: {e}",
            headers={"WWW-Authenticate": "Bearer"},)
