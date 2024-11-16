from pydantic import BaseModel as PydanticBaseModel
from typing import Optional

class ProfesorPydantic(PydanticBaseModel):
    id: int
    nume: str
    prenume: str
    email: str
    grad_didactic: str
    tip_asociere: str
    afiliere: Optional[str]
    class Config:
        from_attributes = True

class StudentPydantic(PydanticBaseModel):
    id:int
    nume: str
    prenume:str
    email: str
    ciclu_studii: str
    an_studiu: int
    grupa: str
    class Config:
        from_attributes = True

class DisciplinaPydantic(PydanticBaseModel):
    cod: str
    id_titular:int
    nume_disciplina:str
    an_studiu: int
    tip_disciplina: str
    categorie_disciplina: str
    tip_examinare: str
    class Config:
        from_attributes = True
