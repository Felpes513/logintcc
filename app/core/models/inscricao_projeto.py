from pydantic import BaseModel

class InscricaoProjeto(BaseModel):
    id_projeto: int
    id_aluno: int
