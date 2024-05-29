import bcrypt
from typing import Optional
import jwt
from datetime import datetime, timedelta
from src.core.config import settings
from src.domain.entity.user_entity import User
from src.infrastructure.security.jwt_handler import JWTHandler
from src.domain.repository.user_repository import IUserRepository


class AuthService:
    """Servicio de autenticación de usuarios."""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
        # Instancia de JWTHandler
        self.jwt_handler = JWTHandler()

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Autentica al usuario con un nombre de usuario y contraseña."""
        user: User = self.user_repository.get_by_username(username)
        if user and self.verify_password(password, user.password):
            return user
        return None

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica que la contraseña ingresada coincida con la contraseña almacenada."""
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    def create_access_token(self, user: User) -> str:
        """Crea un token de acceso JWT para el usuario."""
        payload = {
            "sub": user.id_users,
            "exp": datetime.now() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
            "permissions": user.permissions,
            "username": user.username,
        }
        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return token

    def authenticate_and_generate_token(self, username: str, password: str) -> Optional[str]:
        """Autentica al usuario y genera un token de acceso si la autenticación es exitosa."""
        user = self.authenticate_user(username, password)
        if user:
            return self.create_access_token(user)
        return None
