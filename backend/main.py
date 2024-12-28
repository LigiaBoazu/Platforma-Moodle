from fastapi import *
from peewee import *
from mysql_models import *
from routes import router as routes_router
from database import *
from autentificare_token import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

db.connect()
db.create_tables([Profesor, Student, Disciplina])

app.include_router(routes_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


