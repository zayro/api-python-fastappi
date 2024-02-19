"""IMPORTS."""
import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()


def expire_date(days: int):
    """Detecta si el Token Expiro."""
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date


def write_token(data: dict):
    """Crea un nuevo token."""
    token = jwt.encode(
        payload={**data, "exp": expire_date(2)},
        key=os.getenv("SECRET"),
        algorithm="HS256",
    )
    return token


def validate_token(token):
    """Valida el token."""
    return jwt.decode(token, key=os.getenv("SECRET"), algorithms=["HS256"])
