from fastapi import FastAPI
from fastapi import *
from peewee import MySQLDatabase
from peewee import *
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel as PydanticBaseModel

app = FastAPI()

db = MySQLDatabase('pos', user='ligia', password='ligia', host='localhost', port=3306, **{'charset': 'utf8mb4'})


class BaseModel(Model):
    class Meta:
        database=db

class GradDidactic(str, Enum):
    asis='asist'
    sef_lucr='sef lucr'
    conf='conf'
    prof='prof'

class TipAsociere(str, Enum):
    titular='titular'
    asociat='asociat'
    extern='extern'

class CicluStudii(str, Enum):
    licenta='licenta'
    master='master'

class TipDisciplina(str, Enum):
    impusa='impusa'
    optionala='optionala'
    liber_aleasa='liber aleasa'

class CategorieDisciplina(str, Enum):
    domeniu='domeniu'
    specialitate='specialitate'
    adiacenta='adiacenta'

class TipExaminare(str, Enum):
    examen='examen'
    colocviu='colocviu'

class Profesor(BaseModel):
    id = AutoField(primary_key=True)
    nume = CharField()
    prenume=CharField()
    email = CharField(unique=True)
    grad_didactic=CharField(choices=[(tag.value, tag.value) for tag in GradDidactic], null=False)
    tip_asociere=CharField(choices=[(tag.value, tag.value) for tag in TipAsociere], null=False)
    afiliere=CharField(null=True)
    class Meta:
        db_table = 'Profesori'

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


class Student(BaseModel):
    id = AutoField(primary_key=True)
    nume = CharField()
    prenume=CharField()
    email = CharField(unique=True)
    ciclu_studii=CharField(choices=[(tag.value, tag.value) for tag in CicluStudii], null=False)
    an_studiu=IntegerField(null=False)
    grupa=CharField(null=False)
    class Meta:
        db_table="Studenti"

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

    
class Disciplina(BaseModel):
    cod=CharField(primary_key=True)
    id_titular = ForeignKeyField(Profesor, backref='disciplina', field=Profesor.id, column_name='id_titular')
    nume_disciplina=CharField(null=False)
    an_studiu=IntegerField(null=False)
    tip_disciplina=CharField(choices=[(tag.value, tag. value) for tag in TipDisciplina], null=False)
    categorie_disciplina=CharField(choices=[(tag.value, tag.value) for tag in CategorieDisciplina], null=False)
    tip_examinare=CharField(choices=[(tag.value, tag.value) for tag in TipExaminare], null=False)
    class Meta:
        db_table="Discipline"

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

class StudentDisciplina(BaseModel):
    student=ForeignKeyField(Student, backref='lecture')
    disciplina=ForeignKeyField(Disciplina, backref='students')
    class Meta:
        db_table="Student_Disciplina"
        primary_key=CompositeKey('student', 'disciplina')

class ProfesorDisciplina(BaseModel):
    profesor=ForeignKeyField(Profesor, backref='lecture')
    disciplina=ForeignKeyField(Profesor, backref='professor')
    class Meta:
        db_table="Profesor_Disciplina"
        primary_key=CompositeKey('profesor', 'disciplina')

db.connect()
db.create_tables([Profesor, Student, Disciplina])


@app.get("/api/academia/professors", response_model=List[ProfesorPydantic])
def get_professor(
    grad_didactic: Optional[str]=None,
    nume: Optional[str]=None,
    prenume: Optional[str]=None,
    email: Optional[str]=None,
    tip_asociere: Optional[str]=None,
    afiliere: Optional[str]=None,
    page: Optional[int]=1,
    limit: Optional[int]=20
):
    query=Profesor.select()
    if grad_didactic:
        query=query.where(Profesor.grad_didactic==grad_didactic)
    
    if nume:
        query=query.where(Profesor.nume==nume)
    
    if prenume:
        query=query.where(Profesor.prenume==prenume)
    
    if email:
        query=query.where(Profesor.email==email)

    if tip_asociere:
        query=query.where(Profesor.tip_asociere==tip_asociere)
    
    if afiliere:
        query=query.where(Profesor.afiliere==afiliere)
    
    total = query.count()
    query = query.paginate(page, limit)
    print(total)
    print(query)
    return [ProfesorPydantic.from_orm(professor) for professor in query]

@app.get("/api/academia/students", response_model=List[StudentPydantic])
def get_student(
    nume: Optional[str]=None,
    prenume: Optional[str]=None,
    email: Optional[str]=None,
    ciclu_studii:Optional[str]=None,
    an_studiu:Optional[int]=None,
    grupa:Optional[int]=None,
    page: Optional[int]=1,
    limit: Optional[int]=20
):
    query=Student.select()
    if ciclu_studii:
        query=query.where(Student.ciclu_studii==ciclu_studii)
    
    if nume:
        query=query.where(Student.nume==nume)
    
    if prenume:
        query=query.where(Student.prenume==prenume)
    
    if email:
        query=query.where(Student.email==email)

    if an_studiu:
        query=query.where(Student.an_studiu==an_studiu)
    
    if grupa:
        query=query.where(Student.grupa==grupa)
    
    total = query.count()
    query = query.paginate(page, limit)
    print(total)
    print(query)
    return [StudentPydantic.from_orm(student) for student in query]

@app.get("/api/academia/lectures", response_model=List[DisciplinaPydantic])
def get_lecture(
    cod:Optional[str]=None,
    id_titular: Optional[int] = None,
    nume_disciplina: Optional[str]=None,
    an_studiu:Optional[int]=None,
    tip_disciplina: Optional[str]=None,
    categorie_disciplina: Optional[str]=None,
    tip_examinare: Optional[str]=None,
    page: Optional[int]=1,
    limit: Optional[int]=20
):
    query=Disciplina.select()
    if cod:
        query=query.where(Disciplina.cod==cod)
    
    if id_titular:
        query=query.where(Disciplina.id_titular==id_titular)
    
    if nume_disciplina:
        query=query.where(Disciplina.nume_disciplina==nume_disciplina)
    
    if tip_disciplina:
        query=query.where(Disciplina.tip_disciplina==tip_disciplina)

    if an_studiu:
        query=query.where(Disciplina.an_studiu==an_studiu)
    
    if categorie_disciplina:
        query=query.where(Disciplina.categorie_disciplina==categorie_disciplina)

    if tip_examinare:
        query=query.where(Disciplina.tip_examinare==tip_examinare)
    
    total = query.count()
    query = query.paginate(page, limit)
    print(f"Total records after filtering: {total}")
    print(f"Query after filtering and pagination: {list(query)}")
    return [
        DisciplinaPydantic(
            cod=lecture.cod,
            id_titular=lecture.id_titular.id,
            nume_disciplina=lecture.nume_disciplina,
            an_studiu=lecture.an_studiu,
            tip_disciplina=lecture.tip_disciplina,
            categorie_disciplina=lecture.categorie_disciplina,
            tip_examinare=lecture.tip_examinare
        )
        for lecture in query
    ]


@app.get("/api/academia/professors/{id}/lectures")
def get_professor_lectures(id:int):
    professor=Profesor.get(Profesor.id==id)
    lectures=Disciplina.select().where(Disciplina.id_titular==professor.id)
    return [lecture for lecture in lectures]
    if Profesor.DoesNotExist:
        raise HTTPException(status_code=404, detail="Professor not found")

@app.get("/api/academia/students/{id}/lectures")
def get_student_lectures(id:int):
    student=Student.get(Student.id==id)
    lectures=Disciplina.select().join(StudentDisciplina).where(StudentDisciplina.student==student)
    return [lecture for lecture in lectures]
    if Student.DoesNotExist:
        raise HTTPException(status_code=404, detail="Student not found")




