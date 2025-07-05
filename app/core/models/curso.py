from pydantic import BaseModel

class Curso(BaseModel):
    nome: str  # para entrada (cadastro)

class CursoSchema(BaseModel):
    id_curso: int
    nome: str

    class Config:
        from_attributes = True  # pydantic v2
