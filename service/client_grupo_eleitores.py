from gr import grupo_eleitores_pb2
from gr import grupo_eleitores_pb2_grpc
import grpc

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = grupo_eleitores_pb2_grpc.GrupoEleitoresServiceStub(channel)
        try:
            response = stub.EnviarGrupo(grupo_eleitores_pb2.GrupoRequest(id=1), timeout=5)
            print(response)
        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()} - {e.details()}")

if __name__ == "__main__":
    run()
