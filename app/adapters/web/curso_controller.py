from fastapi import APIRouter, Depends
from typing import List
from app.core.models.curso import Curso, CursoSchema
from app.adapters.repositories.curso_repository import CursoRepository
from app.core.use_cases.create_curso_usecase import CreateCursoUseCase
from app.dependencies import get_db_conn

router = APIRouter(prefix="/cursos", tags=["Cursos"])

@router.post("/")
def cadastrar_curso(curso: Curso, db=Depends(get_db_conn)):
    repo = CursoRepository(db)
    usecase = CreateCursoUseCase(repo)
    curso_id = usecase.execute(curso)
    return {"id": curso_id, "mensagem": "Curso cadastrado com sucesso"}

@router.get("/", response_model=List[CursoSchema])
def get_cursos(db=Depends(get_db_conn)):
    repo = CursoRepository(db)
    return repo.get_all()
