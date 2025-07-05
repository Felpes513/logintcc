from fastapi import APIRouter, Depends, HTTPException
from app.core.models.orientador import Orientador
from app.core.models.secretaria import Secretaria
from app.adapters.repositories.orientador_repository import OrientadorRepository
from app.adapters.repositories.secretaria_repository import SecretariaRepository
from app.core.use_cases.create_orientador_usecase import CreateOrientadorUseCase
from app.core.use_cases.create_secretaria_usecase import CreateSecretariaUseCase
from app.dependencies import get_db_conn

router = APIRouter(tags=["Cadastro"])

@router.post("/register-orientador")
def register_orientador(orientador: Orientador, db=Depends(get_db_conn)):
    repo = OrientadorRepository(db)
    usecase = CreateOrientadorUseCase(repo)

    try:
        orientador_id = usecase.execute(orientador)
        return {
            "id": orientador_id,
            "email": orientador.email,
            "mensagem": "Orientador cadastrado com sucesso"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno no servidor")



# Rota para cadastro de secretaria
@router.post("/register-secretaria")
def register_secretaria(secretaria: Secretaria, db=Depends(get_db_conn)):
    repo = SecretariaRepository(db)
    usecase = CreateSecretariaUseCase(repo)

    try:
        secretaria_id = usecase.execute(secretaria)
        return {
            "id": secretaria_id,
            "email": secretaria.email,
            "mensagem": "Secretaria cadastrada com sucesso"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
