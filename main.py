from fastapi import *
from peewee import *
from mysql_models import *
from routes import router as routes_router
from database import *

app = FastAPI()

db.connect()
db.create_tables([Profesor, Student, Disciplina])

app.include_router(routes_router)


