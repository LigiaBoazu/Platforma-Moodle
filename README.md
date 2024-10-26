# Platforma-Moodle

Aplicație FastAPI ce simulează plaforma educațională Moodle.

## Configurare Docker

Pentru a crea un container Docker pentru baza de date (MariaDB) este suficientă doar crearea unei imagini. Într-un fișier text, se introduc următoarele comenzi:

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

## Instalarea dependințelor necesare

În conda environment-ul creat pentru acest proiect, se instalează dependințele necesare:

```bash
pip install peewee mysqlclient
```

## Rularea aplicației

Rularea aplicației se face din terminalul Visual Studio, folosind comanda:

```bash
uvicorn main:app --reload 
```   
