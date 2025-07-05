from fastapi import APIRouter, HTTPException
from typing import List

from app.adapters.repositories import campus_repository
from app.core.models.campus import CampusSchema, CampusCreate

router = APIRouter(prefix="/campus", tags=["Campus"])

@router.post("/", response_model=dict)
def criar_campus(campus: CampusCreate):
    novo_id = campus_repository.inserir_campus(campus.campus)
    return {"id": novo_id, "mensagem": "Campus inserido com sucesso"}

@router.get("/", response_model=List[CampusSchema])
def listar_campus():
    return campus_repository.listar_campus()

@router.get("/{id_campus}", response_model=CampusSchema)
def buscar_por_id(id_campus: int):
    campus = campus_repository.buscar_campus_por_id(id_campus)
    if not campus:
        raise HTTPException(status_code=404, detail="Campus não encontrado")
    return campus

@router.put("/{id_campus}", response_model=dict)
def atualizar(id_campus: int, nome: str):
    atualizado = campus_repository.atualizar_campus(id_campus, nome)
    if atualizado == 0:
        raise HTTPException(status_code=404, detail="Campus não encontrado para atualização")
    return {"mensagem": "Campus atualizado com sucesso"}

@router.delete("/{id_campus}", response_model=dict)
def deletar(id_campus: int):
    deletado = campus_repository.deletar_campus(id_campus)
    if deletado == 0:
        raise HTTPException(status_code=404, detail="Campus não encontrado para exclusão")
    return {"mensagem": "Campus removido com sucesso"}
