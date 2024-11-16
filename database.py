from peewee import MySQLDatabase
from pymongo import MongoClient

db = MySQLDatabase('pos', user='ligia', password='ligia', host='localhost', port=3306, **{'charset': 'utf8mb4'})
client = MongoClient("mongodb://ligia:ligia@localhost:27017")
test_db = client["mongoDB"]
probe_evaluare_collection=test_db["probe evaluare"]
materiale_curs_collection=test_db["materiale curs"]
materiale_laborator_collection=test_db["materiale laborator"]

probe_evaluare_list=[
    {
        "disciplina": "Programare orientata pe servicii",
        "probe_evaluare":[
            {
                "type":"Laborator",
                "weight":20,
                "description":"Activitatea la laborator"
            },
            {
                "type":"Proiect",
                "weight":30,
                "description":"Activitatea la proiect"
            },
            {
                "type":"Examen",
                "weight":50,
                "description":"Examen in sesiune"
            }
        ],
        "total_weight":100
    },

    {
        "disciplina": "Evaluarea performantelor",
        "probe_evaluare":[
            {
                "type":"Laborator",
                "weight":30,
                "description":"Activitatea la laborator"
            },
            {
                "type":"Proiect",
                "weight":30,
                "description":"Activitatea la proiect"
            },
            {
                "type":"Examen",
                "weight":40,
                "description":"Examen in sesiune"
            }
        ],
        "total_weight":100
    },
    {
        "disciplina": "Algoritmi paraleli si distribuiti",
        "probe_evaluare":[
            {
                "type":"Laborator",
                "weight":20,
                "description":"Activitatea la laborator"
            },
            {
                "type":"Teste",
                "weight":30,
                "description":"Media notelor obtinute la teste"
            },
            {
                "type":"Examen",
                "weight":50,
                "description":"Examen in sesiune"
            }
        ],
        "total_weight":100
    }
]

materiale_curs_list=[
    {
        "disciplina": "Programare orientata pe servicii",
        "materiale_curs":[
            {
                "curs_number":"Curs 1",
                "description":"Introducere in Programarea orientata pe servicii"
            },
            {
                "curs_number":"Curs 2",
                "description":"Servicii WEB SOAP"
            },
            {
                "curs_number":"Curs 3",
                "description":"Servicii Web RESTful"
            }
        ],
    },
    {
        "disciplina": "Evaluarea Performantelor",
        "materiale_curs":[
            {
                "curs_number":"Curs 2024-2025",
                "description":"Curs complet 2024-2025"
            }
        ]
    },
    {
        "disciplina": "Algoritmi paraleli si distribuiti",
        "materiale_curs":[
            {
                "curs_number":"Suport de curs",
                "description":"Curs Algoritmi paraleli si distribuiti 2024-2025"
            }
        ]
    }
]

materiale_laborator_list=[
    {
        "disciplina": "Programare orientata pe servicii",
        "materiale_laborator":[
            {
                "lab_number":"Laborator 1",
                "description":"Descriere si proiectare"
            },
            {
                "lab_number":"Laborator 2",
                "description":"Servicii RESTful pentru baze de date SQL"
            },
            {
                "lab_number":"Laborator 3",
                "description":"Servicii RESTful pentru baze de date NoSQL"
            }
        ]
    },
    {
        "disciplina": "Evaluarea Performantelor",
        "materiale_laborator":[
            {
                "lab_number":"Suport laborator",
                "description":"Suport complet 2024-2025"
            }
        ]
    },
    {
        "disciplina": "Algoritmi paraleli si distribuiti",
        "materiale_laborator":[
            {
                "lab_number":"Laborator 1",
                "description":"Introducere in OpenMP"
            },
            {
                "lab_number":"Laborator 2",
                "description":"Introducere in MPI"
            }
        ]
    }
]

for probe_evaluare in probe_evaluare_list:
    existing_document = probe_evaluare_collection.find_one({"disciplina": probe_evaluare["disciplina"]})
    if existing_document is None:
        probe_evaluare_collection.insert_one(probe_evaluare)
        print(f"Document for {probe_evaluare['disciplina']} inserted.")
    else:
        print(f"Document for {probe_evaluare['disciplina']} already exists.")

for materiale_curs in materiale_curs_list:
    existing_document=materiale_curs_collection.find_one({"disciplina": materiale_curs["disciplina"]})
    if existing_document:
        materiale_curs_collection.update_one(
            {"disciplina": materiale_curs["disciplina"]},
            {"$addToSet": {"materiale_curs": {"$each": materiale_curs["materiale_curs"]}}}
        )
        print(f"Courses for {materiale_curs['disciplina']} updated.")
    else:
        materiale_curs_collection.insert_one(materiale_curs)
        print(f"Document for {materiale_curs['disciplina']} inserted.")

for materiale_lab in materiale_laborator_list:
    existing_document = materiale_laborator_collection.find_one({"disciplina": materiale_lab["disciplina"]})
    if existing_document:
        materiale_laborator_collection.update_one(
            {"disciplina": materiale_lab["disciplina"]},
            {"$addToSet": {"materiale_laborator": {"$each": materiale_lab["materiale_laborator"]}}}
        )
        print(f"Laboratories for {materiale_lab['disciplina']} updated.")
    else:
        materiale_laborator_collection.insert_one(materiale_lab)
        print(f"Laboratories for {materiale_lab['disciplina']} inserted.")

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

duplicates_curs = list(materiale_curs_collection.aggregate(pipeline))
for duplicate in duplicates_curs:
    ids_to_delete = duplicate["uniqueIds"][1:]
    materiale_curs_collection.delete_many({"_id": {"$in": ids_to_delete}})
    print(f"Deleted duplicates for disciplina: {duplicate['_id']}")

duplicates_lab = list(materiale_laborator_collection.aggregate(pipeline))
for duplicate in duplicates_lab:
    ids_to_delete = duplicate["uniqueIds"][1:]
    materiale_laborator_collection.delete_many({"_id": {"$in": ids_to_delete}})
    print(f"Deleted duplicates for disciplina: {duplicate['_id']}")

duplicates_probe_evaluare = list(probe_evaluare_collection.aggregate(pipeline))
for duplicate in duplicates_probe_evaluare:
    ids_to_delete = duplicate["uniqueIds"][1:]
    probe_evaluare_collection.delete_many({"_id": {"$in": ids_to_delete}})
    print(f"Deleted duplicates for disciplina: {duplicate['_id']}")

print("Duplicate removal completed.")