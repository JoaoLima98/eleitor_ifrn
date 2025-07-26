import grpc
from concurrent import futures
import time

from gr import grupo_eleitores_pb2_grpc
from handlers.grupo_eleitores_handler import GrupoEleitoresGrpcHandler
from service.grupo_eleitores_service import GrupoEleitoresService
from repository.grupo_eleitores_repository import GrupoEleitoresRepository
from infra.db import get_session  # Ajuste isso para sua factory de Session

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    db = next(get_session())  # ou SessionLocal()
    grupo_repository = GrupoEleitoresRepository(db)
    grupo_service = GrupoEleitoresService(grupo_repository)

    handler = GrupoEleitoresGrpcHandler(grupo_service)
    grupo_eleitores_pb2_grpc.add_GrupoEleitoresServiceServicer_to_server(handler, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC rodando na porta 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
