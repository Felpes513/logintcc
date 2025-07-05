from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from app.adapters.repositories.inscricao_projeto_repository import InscricaoRepository
from app.core.use_cases.inscrever_aluno_usecase import InscreverAlunoUseCase
from app.core.use_cases.listar_inscricoes_usecase import ListarInscricoesPorProjetoUseCase
import os
import shutil



from app.dependencies import get_db_conn

router = APIRouter(prefix="/inscricoes", tags=["Inscrições"])

@router.post("/")
def inscrever_aluno(
    id_projeto: int = Form(...),
    id_aluno: int = Form(...),
    arquivo_pdf: UploadFile = File(...),
    db=Depends(get_db_conn)
):
    repo = InscricaoRepository(db)
    usecase = InscreverAlunoUseCase(repo)
    try:
        usecase.execute(id_projeto, id_aluno, arquivo_pdf)
        return {"mensagem": "Inscrição realizada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro inesperado: " + str(e))

@router.get("/projetos/{id_projeto}/inscricoes")
def listar_inscricoes_por_projeto(id_projeto: int, db=Depends(get_db_conn)):
    repo = InscricaoRepository(db)
    usecase = ListarInscricoesPorProjetoUseCase(repo)
    try:
        return usecase.execute(id_projeto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/aprovar/{id_inscricao}")
def aprovar_inscricao(id_inscricao: int, db=Depends(get_db_conn)):
    repo = InscricaoRepository(db)
    try:
        repo.aprovar_inscricao(id_inscricao)
        return {"mensagem": "Aluno aprovado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/excluir/{id_inscricao}")
def excluir_inscricao(id_inscricao: int, db=Depends(get_db_conn)):
    repo = InscricaoRepository(db)
    try:
        repo.excluir_inscricao(id_inscricao)
        return {"mensagem": "Inscrição removida com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

