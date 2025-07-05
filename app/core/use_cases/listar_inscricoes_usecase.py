class ListarInscricoesPorProjetoUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, id_projeto: int):
        if not isinstance(id_projeto, int) or id_projeto <= 0:
            raise ValueError("ID do projeto inválido")

        inscricoes = self.repo.listar_inscricoes_por_projeto(id_projeto)

        if not inscricoes:
            print(f"📭 Nenhuma inscrição encontrada para o projeto {id_projeto}")

        return inscricoes
