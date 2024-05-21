from datetime import datetime, timedelta
from typing import Optional
import jwt
from src.core.config import settings


class JWTHandler:
    def __init__(self):
        # Llave secreta para firmar los tokens JWT, configurada en settings
        self.secret_key = settings.JWT_SECRET_KEY
        # Algoritmo utilizado para firmar los tokens JWT, configurado en settings
        self.algorithm = settings.JWT_ALGORITHM

    def create_token(self, user_id: int) -> str:
        """
        Crea un token JWT para un usuario específico.

        Args:
            user_id (int): ID del usuario para el que se creará el token.

        Returns:
            str: Token JWT generado.
        """
        expiration = datetime.now() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        payload = {
            "sub": user_id,
            "exp": expiration,
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def verify_token(self, token: str) -> Optional[int]:
        """
        Verifica un token JWT.

        Args:
            token (str): Token JWT que se verificará.

        Returns:
            Optional[int]: ID del usuario si el token es válido, None de lo contrario.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload.get("sub")
        except jwt.ExpiredSignatureError:
            # El token ha expirado
            return None
        except jwt.InvalidTokenError:
            # El token es inválido
            return None
