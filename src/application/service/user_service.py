from typing import List, Optional
from src.domain.entity.user_entity import User
from src.infrastructure.database.user_repository import UserRepository
from src.application.use_case.user_use_case import UserUseCase


class UserService:
    """Servicio de la entidad User."""

    user_use_case: UserUseCase

    def __init__(self):
        repository = UserRepository()
        self.user_use_case = UserUseCase(repository)

    def get_all_users(self) -> List[User]:
        """
        Obtiene una lista de todos los usuarios.
        """
        return self.user_use_case.get_all_users()

    def create_user(self, user_create: User) -> Optional[User]:
        """
        Crea un nuevo usuario.
        """
        return self.user_use_case.create_user(user_create)
