import grpc
from concurrent import futures
import autentificare_pb2
import autentificare_pb2_grpc
from peewee import *
from mysql_models import Utilizatori

db = MySQLDatabase('pos', user='ligia', password='ligia', host='localhost', port=3306)
 
class AutentificareService(autentificare_pb2_grpc.AutentificareServicer):
    def Cerere(self, request, context):
        print(f"Received authentication request for email: {request.email}")
        try:
            utilizator = Utilizatori.get(Utilizatori.email == request.email)
            if utilizator.parola == request.parola:
                token = f"Token_{utilizator.id}"
                print(f"Authentication successful for {utilizator.email}, token generated: {token}")
                return autentificare_pb2.Response(token=token)
            else:
                context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                context.set_details("Incorrect password")
                print(f"Incorrect password for {utilizator.email}")
                return autentificare_pb2.Response()
        except Utilizatori.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not registered")
            print(f"User with email {request.email} not found in the database")
            return autentificare_pb2.Response()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    autentificare_pb2_grpc.add_AutentificareServicer_to_server(AutentificareService(), server)
    server.add_insecure_port('[::]:50051')
    print("Serverul ruleaza pe portul 50051")
    server.start()
    server.wait_for_termination()



if __name__ == "__main__":
    serve()
