from app.core.models.aluno import Aluno
from app.core.ports.output.porta_aluno_repository import IAlunoRepository

class CreateAlunoUseCase:
    def __init__(self, repo: IAlunoRepository):
        self.repo = repo

    def execute(self, aluno: Aluno) -> int:
        return self.repo.create(aluno)