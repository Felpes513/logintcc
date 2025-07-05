from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.core.models.orientador import Orientador, OrientadorSchema
from app.adapters.repositories.orientador_repository import OrientadorRepository
from app.core.use_cases.create_orientador_usecase import CreateOrientadorUseCase
from app.dependencies import get_db_conn

router = APIRouter(prefix="/orientadores", tags=["Orientadores"])

@router.post("/", status_code=201)
def cadastrar_orientador(orientador: Orientador, db=Depends(get_db_conn)):
    repo = OrientadorRepository(db)
    usecase = CreateOrientadorUseCase(repo)
    try:
        orientador_id = usecase.execute(orientador)
        return {"id": orientador_id, "mensagem": "Orientador cadastrado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro inesperado no servidor")

@router.get("/", response_model=List[OrientadorSchema])
def listar_orientadores(db=Depends(get_db_conn)):
    repo = OrientadorRepository(db)
    return repo.listar_orientadores()

@router.get("/buscar")
def buscar_orientador_por_nome(nome: str, db=Depends(get_db_conn)):
    repo = OrientadorRepository(db)
    orientadores = repo.listar_orientadores()

    nome_normalizado = nome.strip().lower()

    # Logs para depuração
    print("🧪 Buscando por nome:", nome_normalizado)
    print("🔍 Nomes no banco:")
    for o in orientadores:
        print(" -", o["nome_completo"].strip().lower())

    # Busca insensível a maiúsculas/minúsculas e espaços
    orientador = next(
        (o for o in orientadores if o["nome_completo"].strip().lower() == nome_normalizado),
        None
    )

    if not orientador:
        raise HTTPException(status_code=404, detail="Orientador não encontrado")
    return orientador


