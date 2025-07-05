from app.core.models.orientador import Orientador
from app.adapters.repositories.orientador_repository import OrientadorRepository

class CreateOrientadorUseCase:
    def __init__(self, repo: OrientadorRepository):
        self.repo = repo

    def execute(self, orientador: Orientador) -> int:
        return self.repo.create(orientador)
