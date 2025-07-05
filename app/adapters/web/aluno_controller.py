from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.adapters.repositories.aluno_repository import AlunoRepository
from app.core.models.aluno import AlunoSchema
from app.dependencies import get_db_conn

router = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.get("/", response_model=List[AlunoSchema])
def listar_alunos(db=Depends(get_db_conn)):
    repo = AlunoRepository(db)
    return repo.get_all()

@router.get("/{id_aluno}", response_model=AlunoSchema)
def buscar_aluno_por_id(id_aluno: int, db=Depends(get_db_conn)):
    repo = AlunoRepository(db)
    aluno = repo.get_by_id(id_aluno)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno
