from pydantic import BaseModel

class CampusCreate(BaseModel):
    campus: str  # apenas o campo necessário para criar

class CampusSchema(CampusCreate):
    id: int

    class Config:
        from_attributes = True  # ou orm_mode = True se estiver com Pydantic v1
