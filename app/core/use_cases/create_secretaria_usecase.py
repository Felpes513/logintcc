from app.core.models.secretaria import Secretaria
from app.adapters.repositories.secretaria_repository import SecretariaRepository

class CreateSecretariaUseCase:
    def __init__(self, repo: SecretariaRepository):
        self.repo = repo

    def execute(self, secretaria: Secretaria) -> int:
        senha_hash = secretaria.gerar_hash()
        return self.repo.create(secretaria, senha_hash)
