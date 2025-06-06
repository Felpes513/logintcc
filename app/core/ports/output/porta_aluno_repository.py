from abc import ABC, abstractmethod
from app.core.models.aluno import Aluno

class IAlunoRepository(ABC):
    @abstractmethod
    def create(self, aluno: Aluno) -> int:
        pass
