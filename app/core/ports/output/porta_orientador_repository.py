from abc import ABC, abstractmethod
from app.core.models.orientador import Orientador

class IOrientadorRepository(ABC):
    @abstractmethod
    def create(self, orientador: Orientador) -> int:
        pass
