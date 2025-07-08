from abc import ABC, abstractmethod

class RelatorioRepositoryPort(ABC):
    @abstractmethod
    def salvar_relatorio(self, dados): pass

    @abstractmethod
    def buscar_por_aluno(self, aluno_id: int): pass
