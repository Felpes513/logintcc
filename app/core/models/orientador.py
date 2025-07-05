import re
from typing import Annotated, List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, constr
from app.core.security import gerar_hash_senha

# 🔹 1. Pydantic - Entrada (validação + lógica de domínio)
class Orientador(BaseModel):
    nome_completo: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    cpf: str = Field(
        ...,
        pattern=r"^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$",
        description="CPF no formato xxx.xxx.xxx-xx ou como 11 dígitos"
    )
    senha: Annotated[str, constr(min_length=6)]
    cursos: Optional[List[int]] = []

    @property
    def senha_hash(self) -> str:
        return gerar_hash_senha(self.senha)

    @field_validator('cpf')
    def cpf_valido(cls, v):
        cpf = re.sub(r'\D', '', v)
        if len(set(cpf)) == 1 or len(cpf) != 11:
            raise ValueError("CPF inválido")

        def calc_digito(digs):
            s = sum(int(d) * i for d, i in zip(digs, range(len(digs) + 1, 1, -1)))
            r = (s * 10) % 11
            return '0' if r == 10 else str(r)

        if cpf[-2] != calc_digito(cpf[:9]) or cpf[-1] != calc_digito(cpf[:10]):
            raise ValueError("CPF inválido")

        return cpf
class OrientadorSchema(BaseModel):
    id: int
    nome_completo: str
    email: EmailStr

    class Config:
        from_attributes = True
