from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entity.user_entity import User


class IUserRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def create(self) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError
