import grpc
from concurrent import futures
import autentificare_pb2_grpc
import autentificare_pb2
from peewee import *
from mysql_models import Utilizatori

db = MySQLDatabase('pos', user='ligia', password='ligia', host='localhost', port=3306, **{'charset': 'utf8mb4'})

def run():
    utilizator = Utilizatori.select().first() 
    if utilizator:
        email = utilizator.email
        parola = utilizator.parola
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = autentificare_pb2_grpc.AutentificareStub(channel)
            authentication_request = autentificare_pb2.Credentials(email=email, parola=parola)
            try:
                response = stub.CerereAutentificare(authentication_request)
                if response.token:
                    print(f"Autentificare reușita! Token: {response.token}")
                else:
                    print("Autentificare nereusita!")
            except grpc.RpcError as e:
                print(f"Eroare la comunicarea cu serverul: {e}")
    else:
        print("Nu exista utilizatori in baza de date!")
            