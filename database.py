from peewee import MySQLDatabase
from pymongo import MongoClient

db = MySQLDatabase('pos', user='ligia', password='ligia', host='localhost', port=3306, **{'charset': 'utf8mb4'})
client = MongoClient("mongodb://ligia:ligia@localhost:27017")
test_db = client["mongoDB"]
discipline_collection=test_db["discipline"]

discipline_list = [
    {
        "disciplina": "Programare orientata pe servicii",
        "probe_evaluare": [
            {"type": "Laborator", "weight": 20, "description": "Activitatea la laborator"},
            {"type": "Proiect", "weight": 30, "description": "Activitatea la proiect"},
            {"type": "Examen", "weight": 50, "description": "Examen in sesiune"}
        ],
        "materiale_curs": [
            {"curs_number": "Curs 1", "description": "Introducere in Programarea orientata pe servicii"},
            {"curs_number": "Curs 2", "description": "Servicii WEB SOAP"},
            {"curs_number": "Curs 3", "description": "Servicii Web RESTful"}
        ],
        "materiale_laborator": [
            {"lab_number": "Laborator 1", "description": "Descriere si proiectare"},
            {"lab_number": "Laborator 2", "description": "Servicii RESTful pentru baze de date SQL"},
            {"lab_number": "Laborator 3", "description": "Servicii RESTful pentru baze de date NoSQL"}
        ]
    },
    {
        "disciplina": "Evaluarea Performantelor",
        "probe_evaluare": [
            {"type": "Laborator", "weight": 30, "description": "Activitatea la laborator"},
            {"type": "Proiect", "weight": 30, "description": "Activitatea la proiect"},
            {"type": "Examen", "weight": 40, "description": "Examen in sesiune"}
        ],
        "materiale_curs": [
            {"curs_number": "Curs 2024-2025", "description": "Curs complet 2024-2025"}
        ],
        "materiale_laborator": [
            {"lab_number": "Suport laborator", "description": "Suport complet 2024-2025"}
        ]
    },
    {
        "disciplina": "Algoritmi paraleli si distribuiti",
        "probe_evaluare": [
            {"type": "Laborator", "weight": 20, "description": "Activitatea la laborator"},
            {"type": "Teste", "weight": 30, "description": "Media notelor obtinute la teste"},
            {"type": "Examen", "weight": 50, "description": "Examen in sesiune"}
        ],
        "materiale_curs": [
            {"curs_number": "Suport de curs", "description": "Curs Algoritmi paraleli si distribuiti 2024-2025"}
        ],
        "materiale_laborator": [
            {"lab_number": "Laborator 1", "description": "Introducere in OpenMP"},
            {"lab_number": "Laborator 2", "description": "Introducere in MPI"}
        ]
    }
]

for disciplina in discipline_list:
    existing_document = discipline_collection.find_one({"disciplina": disciplina["disciplina"]})
    if existing_document:
        discipline_collection.update_one(
            {"disciplina": disciplina["disciplina"]},
            {"$set": {
                "probe_evaluare": disciplina["probe_evaluare"],
                "materiale_curs": disciplina["materiale_curs"],
                "materiale_laborator": disciplina["materiale_laborator"]
            }}
        )
        print(f"Document for {disciplina['disciplina']} updated.")
    else:
        discipline_collection.insert_one(disciplina)
        print(f"Document for {disciplina['disciplina']} inserted.")

pipeline = [
    {"$group": {
        "_id": "$disciplina",  
        "uniqueIds": {"$addToSet": "$_id"},  
        "count": {"$sum": 1} 
    }},
    {"$match": {
        "count": {"$gt": 1}
    }}
]

duplicates_discipline = list(discipline_collection.aggregate(pipeline))
for duplicate in duplicates_discipline:
    ids_to_delete = duplicate["uniqueIds"][1:]
    discipline_collection.delete_many({"_id": {"$in": ids_to_delete}})
    print(f"Deleted duplicates for disciplina: {duplicate['_id']}")

print("Duplicate removal completed.")