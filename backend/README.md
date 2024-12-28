# Platforma-Moodle

Aplicație FastAPI ce simulează plaforma educațională Moodle.

## Configurare Docker

Pentru a crea un container Docker pentru baza de date MariaDB este suficientă doar crearea unei imagini. Într-un fișier text, se introduc următoarele comenzi:

```dockerfile
   FROM mariadb:latest
   ENV MYSQL_ROOT_PASSWORD=password
   ENV MYSQL_DATABASE=pos
   ENV MYSQL_USER=user
   ENV MYSQL_PASSWORD=pass
   EXPOSE 3306
```

Pentru a construi și rula imaginea pe care dorim să o creăm, trebuie să rulăm următoarele comenzi:

 ```bash
docker build-t mariadb-demo .
docker run-d-p 3306:3306–name mariadb-container mariadb-demo
```

Pentru a crea un container Docker pentru baza de date MongoDB, se crează un fișier docker-build.yml, în care se introduc următoarele comenzi:

```services:
  mongodb:
    image: mongo:latest
    container_name: mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: user
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

Pentru a construi și rula imaginea pe care dorim să o creăm, trebuie să rulăm următoarele comenzi:

 ```bash
docker-compose up --build
```

## Instalarea dependințelor necesare

În conda environment-ul creat pentru acest proiect, se instalează dependințele necesare:

```bash
pip install peewee mysqlclient
pip install pymongo
```

## Verificarea colecțiilor în MongoDB

Pentru a verifica colecțiile create în Mongo, se pot rula următoarele comenzi:

```bash
mongosh "mongodb://[path]"
show databases
use mongoDB
show collections
db["discipline"].find()
```

## Crearea unui serviciu gRPC

În prima etapă, se creează un fișier .proto care definește interfața serviciului gRPC și tipurile de date pe care le vei folosi pentru a comunica între client și server. Acest fișier specifică:
- mesajele (structurile de date) ce sunt trimise și primite
- serviciile (funcțiile sau RPC-urile), care sunt disponibile pentru a fi apelate de client și server.

În continuare sunt prezentate comenzile necesare pentru instalarea pachetului grpcio-tools și pentru a genera fișierele Python care conțin definițiile Protobuf (mesajele definite în fișierul .proto):

```bash
conda activate moodle
pip install grpcio_tools
python -m grpc_tools.protoc -I=[directorul în care se află fișierul .proto] --python_out=. --grpc_python_out=. autentificare.proto
```  

## Rularea aplicației

Rularea aplicației se face din terminalul Visual Studio, folosind comanda:

```bash
uvicorn main:app --reload 
```  

În cazul în care nu se poate porni container-ul docker, verificați dacă există vreun proces care folosește portul respectiv și eliminați-l, folosind comenzile:

```bash
netstat -ano | findstr :3306
taskkill /PID [nr_proces] /F
```  


