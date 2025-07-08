from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from app.dependencies.db import get_db_conn as get_db
from app.adapters.repositories.relatorio_repository import gerar_relatorio_alunos_aprovados, gerar_relatorio_projeto_especifico, gerar_relatorio_todos_projetos

router = APIRouter(prefix="/relatorios", tags=["Relatórios Excel"])

@router.get("/excel/alunos-aprovados", summary="Exportar alunos aprovados em Excel")
def exportar_alunos_aprovados_excel(db=Depends(get_db)):
    try:
        caminho = gerar_relatorio_alunos_aprovados(db)
        nome_arquivo = caminho.split("/")[-1] 
        return FileResponse(
            path=caminho,
            filename=nome_arquivo,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/excel/projeto", summary="Gerar relatório de um projeto específico")
def exportar_projeto_excel(
    titulo: str = None,
    orientador: str = None,
    numero_projeto: str = None,
    db=Depends(get_db)
):
    try:
        caminho = gerar_relatorio_projeto_especifico(
            db,
            titulo=titulo,
            orientador=orientador,
            numero_projeto=numero_projeto
        )
        nome_arquivo = caminho.split("/")[-1]  # ou .split("\\")[-1] no Windows
        return FileResponse(
            path=caminho,
            filename=nome_arquivo,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/excel/projetos", summary="Gerar relatório de todos os projetos")
def exportar_todos_projetos_excel(db=Depends(get_db)):
    try:
        caminho = gerar_relatorio_todos_projetos(db)
        nome_arquivo = caminho.split("/")[-1]
        return FileResponse(
            path=caminho,
            filename=nome_arquivo,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
