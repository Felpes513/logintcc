from app.core.models.secretaria import Secretaria
from app.adapters.repositories.secretaria_repository import SecretariaRepository

class CreateSecretariaUseCase:
    def __init__(self, repo: SecretariaRepository):
        self.repo = repo

    def execute(self, secretaria: Secretaria) -> int:
        return self.repo.create(secretaria)
