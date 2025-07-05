from pydantic import BaseModel

class CampusSchema(BaseModel):
    id: int
    campus: str

    class Config:
        orm_mode = True
