from typing import List
from src.domain.entity.user_entity import User
from src.domain.repository.user_repository import IUserRepository

# from app.schemas.user_schemas import UserCreate, UserResponse


class UserUseCase:
    """Caso de uso para la entidad User."""

    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def create_user(self, user_create: User):
        """Crea un nuevo usuario."""
        user = User(
            id_users=None,
            username=user_create.username,
            email=user_create.email,
            password=user_create.password,
        )
        new_user = self.repository.create(user)
        return new_user

    def get_all_users(self):
        """Obtiene todos los usuarios."""
        users = self.repository.get_all()
        return users

    def get_by_username(self, username: str):
        """Obtiene todos los usuarios."""
        users = self.repository.get_by_username(username)
        return users

    # Otros casos de uso relacionados con usuarios...
