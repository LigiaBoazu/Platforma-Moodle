from peewee import *
from database import db
from enumerations import *

class BaseModel(Model):
    class Meta:
        database=db

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