from abc import ABC, abstractmethod
from app.core.models.curso import Curso

class ICursoRepository(ABC):
    @abstractmethod
    def create(self, curso: Curso) -> int:
        pass

    @abstractmethod
    def get_all(self) -> list[dict]:
        pass
