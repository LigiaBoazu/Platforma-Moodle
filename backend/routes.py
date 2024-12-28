import logging
from fastapi import *
from peewee import *
from typing import List, Optional
from autentificare_token import create_token, validate_token
from pydantic_models import *
from mysql_models import *
from database import discipline_collection
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/api/academia/professors", response_model=List[ProfesorPydantic])
def get_professor(
    grad_didactic: Optional[str]=None,
    nume: Optional[str]=None,
    prenume: Optional[str]=None,
    email: Optional[str]=None,
    tip_asociere: Optional[str]=None,
    afiliere: Optional[str]=None,
    page: Optional[int]=1,
    limit: Optional[int]=20,
    token: str=Depends(oauth2_scheme)
):
    user_data = validate_token(token)
    if user_data["role"] not in ["admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
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
    return [ProfesorPydantic(**professor.__data__) for professor in query]

@router.get("/api/academia/students", response_model=List[StudentPydantic])
def get_student(
    nume: Optional[str]=None,
    prenume: Optional[str]=None,
    email: Optional[str]=None,
    ciclu_studii:Optional[str]=None,
    an_studiu:Optional[int]=None,
    grupa:Optional[int]=None,
    page: Optional[int]=1,
    limit: Optional[int]=20,
    token: str=Depends(oauth2_scheme)
):
    
    user_data = validate_token(token)
    if user_data["role"] not in ["profesor", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
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

@router.get("/api/academia/lectures", response_model=List[DisciplinaPydantic])
def get_lecture(
    cod:Optional[str]=None,
    id_titular: Optional[int] = None,
    nume_disciplina: Optional[str]=None,
    an_studiu:Optional[int]=None,
    tip_disciplina: Optional[str]=None,
    categorie_disciplina: Optional[str]=None,
    tip_examinare: Optional[str]=None,
    page: Optional[int]=1,
    limit: Optional[int]=20,
    username: str=Depends(validate_token),
    token: str = Depends(oauth2_scheme)
):
    user_data = validate_token(token)
    if user_data["role"] not in ["profesor", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
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


@router.get("/api/academia/professors/{id}/lectures")
def get_professor_lectures(id:int, token: str = Depends(oauth2_scheme)):
    user_data = validate_token(token)
    if user_data["role"] not in ["admin", "profesor"]:
        raise HTTPException(status_code=403, detail="Access denied")
    professor=Profesor.get(Profesor.id==id)
    lectures=Disciplina.select().where(Disciplina.id_titular==professor.id)
    return [lecture for lecture in lectures]
    if Profesor.DoesNotExist:
        raise HTTPException(status_code=404, detail="Professor not found")

@router.get("/api/academia/students/{id}/lectures")
def get_student_lectures(id:int, token: str = Depends(oauth2_scheme)):
    user_data = validate_token(token)
    if user_data["role"] not in ["admin", "student"]:
        raise HTTPException(status_code=403, detail="Access denied")
    student=Student.get(Student.id==id)
    lectures=Disciplina.select().join(StudentDisciplina).where(StudentDisciplina.student==student)
    return [lecture for lecture in lectures]
    if Student.DoesNotExist:
        raise HTTPException(status_code=404, detail="Student not found")

@router.put("/api/academia/lectures/{lecture_id}", response_model=DisciplinaPydantic)
def create_lecture(lecture_id: str, lecture_info: CreareDisciplinaPydantic, token: str = Depends(oauth2_scheme)):
    user_data = validate_token(token)
    if user_data["role"] not in ["admin", "profesor"]:
        raise HTTPException(status_code=403, detail="Access denied")
    try:
        profesor = Profesor.get(Profesor.id == lecture_info.id_titular)
    except Profesor.DoesNotExist:
        raise HTTPException(status_code=404, detail="Professor not found")

    if Disciplina.select().where(Disciplina.cod == lecture_id).exists():
        raise HTTPException(status_code=400, detail="A lecture with this code already exists")

    try:
        disciplina = Disciplina.create(
            cod=lecture_id,
            id_titular=lecture_info.id_titular,
            nume_disciplina=lecture_info.nume_disciplina,
            an_studiu=lecture_info.an_studiu,
            tip_disciplina=lecture_info.tip_disciplina,
            categorie_disciplina=lecture_info.categorie_disciplina,
            tip_examinare=lecture_info.tip_examinare
        )
    except IntegrityError as e:
        logging.error(f"Error creating the lecture: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Couldn't create the lecture: {str(e)}")

    response_data = DisciplinaPydantic.from_orm(disciplina)

    try:
        discipline_document={
            "disciplina": lecture_info.nume_disciplina,
            "probe_evaluare": [
                {
                    "type": probe.tip_evaluare,
                    "weight": probe.pondere,
                    "description": probe.description
                } for probe in lecture_info.proba_evaluare
            ],
            "materiale_curs": [
                {
                    "curs_number": curs.curs_number,
                    "curs_name": curs.curs_name,
                    "path_file": curs.path_file
                } for curs in lecture_info.materiale_curs
            ],
            "materiale_laborator":[
                {
                    "lab_number": lab.lab_number,
                    "curs_name": lab.curs_name,
                    "path_file": lab.path_file
                } for lab in lecture_info.materiale_lab
            ]
        }
        discipline_collection.insert_one(discipline_document)
    
    except Exception:
        logging.error("Error in inserting additional documents")
        raise HTTPException(status_code=500, detail="Error in inserting additional documents")

    return response_data

@router.post("/api/academia/login")
def login(credentials: LoginPydantic):
    try:
        user = Utilizatori.get((Utilizatori.email == credentials.username) & (Utilizatori.parola == credentials.password))
        token = create_token(data={"sub": user.email, "role": user.rol})
        return {"access_token": token}
    except Utilizatori.DoesNotExist:
        raise HTTPException(status_code=401, detail="Incorrect credentials")
