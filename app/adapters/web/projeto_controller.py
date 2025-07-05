from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.adapters.repositories import campus_repository
from app.core.models.campus import CampusSchema
from app.core.models.orientador import OrientadorSchema
from app.core.models.projeto import Projeto
from app.adapters.repositories.projeto_repository import ProjetoRepository
from app.core.use_cases.create_projeto_usecase import CreateProjetoUseCase

from app.dependencies import get_db_conn  # único usado

router = APIRouter(prefix="/projetos", tags=["Projetos"])

# ==== ROTAS DE PROJETO ====
@router.post("/")
def cadastrar_projeto(projeto: Projeto, db=Depends(get_db_conn)):
    repo = ProjetoRepository(db)
    usecase = CreateProjetoUseCase(repo)
    try:
        projeto_id = usecase.execute(projeto)
        return {"id": projeto_id, "mensagem": "Projeto cadastrado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro inesperado")

@router.get("/")
def listar_projetos(db=Depends(get_db_conn)):
    repo = ProjetoRepository(db)
    try:
        return repo.listar_todos()
    except Exception as e:
        print("❌ Erro ao listar projetos:", e)
        raise HTTPException(status_code=500, detail="Erro ao listar projetos")

@router.get("/{id_projeto}")
def buscar_projeto(id_projeto: int, db=Depends(get_db_conn)):
    repo = ProjetoRepository(db)
    try:
        return repo.buscar_por_id(id_projeto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print("❌ Erro ao buscar projeto:", e)
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.put("/{id_projeto}")
def atualizar_projeto(id_projeto: int, projeto: Projeto, db=Depends(get_db_conn)):
    repo = ProjetoRepository(db)
    try:
        repo.atualizar(id_projeto, projeto)
        return {"mensagem": "Projeto atualizado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print("❌ Erro ao atualizar projeto:", e)
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.delete("/{id_projeto}")
def deletar_projeto(id_projeto: int, db=Depends(get_db_conn)):
    repo = ProjetoRepository(db)
    try:
        repo.deletar(id_projeto)
        return {"mensagem": "Projeto excluído com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print("❌ Erro ao deletar projeto:", e)
        raise HTTPException(status_code=500, detail="Erro interno do servidor")