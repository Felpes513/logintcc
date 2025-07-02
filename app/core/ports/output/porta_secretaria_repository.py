from abc import ABC, abstractmethod
from app.core.models.secretaria import Secretaria

class ISecretariaRepository(ABC):
    @abstractmethod
    def create(self, secretaria: Secretaria) -> int:
        pass
