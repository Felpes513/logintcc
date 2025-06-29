from pydantic import BaseModel, EmailStr, Field, constr

class Secretaria(BaseModel):
    nome_completo: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    senha: str = Field(..., min_length=6)

    @property
    def senha_hash(self) -> str:
        from app.core.security import gerar_hash_senha
        return gerar_hash_senha(self.senha)
