from pydantic import BaseModel as PydanticBaseModel
from typing import List, Optional

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

class ProbaEvaluarePydantic(PydanticBaseModel):
    tip_evaluare: str
    pondere: int
    description: str

class MaterialeCursPydantic(PydanticBaseModel):
    curs_number: int
    curs_name: str
    path_file: str

class MaterialeLaboratorPydantic(PydanticBaseModel):
    lab_number: int
    curs_name: str
    path_file: str

class CreareDisciplinaPydantic(PydanticBaseModel):
    cod: str
    nume_disciplina:str
    id_titular: int
    an_studiu: int
    tip_disciplina: str
    categorie_disciplina: str
    tip_examinare: str
    proba_evaluare: Optional[List[ProbaEvaluarePydantic]]=None
    materiale_curs: Optional[List[MaterialeCursPydantic]]=None
    materiale_lab: Optional[List[MaterialeLaboratorPydantic]]=None