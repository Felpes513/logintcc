from fastapi import APIRouter, Depends, HTTPException
from app.core.models.secretaria import Secretaria
from app.adapters.repositories.secretaria_repository import SecretariaRepository
from app.core.use_cases.create_secretaria_usecase import CreateSecretariaUseCase
from app.dependencies import get_db_conn

router = APIRouter(prefix="/secretarias", tags=["Secretarias"])

@router.post("/")
def cadastrar_secretaria(secretaria: Secretaria, db=Depends(get_db_conn)):
    repo = SecretariaRepository(db)
    usecase = CreateSecretariaUseCase(repo)

    try:
        secretaria_id = usecase.execute(secretaria)
        return {"id": secretaria_id, "mensagem": "Secretaria cadastrada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        print("❌ Erro inesperado:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro inesperado no servidor")
