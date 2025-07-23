import grpc
from gr import elegivel_pb2, elegivel_pb2_grpc

def run():
    with grpc.insecure_channel('18.118.122.201:8000') as channel:
        stub = elegivel_pb2_grpc.ElegivelServiceStub(channel)

        curso = elegivel_pb2.Curso(
            id=1,
            nome="Engenharia",
            descricao="Curso de Engenharia",
            etapa=elegivel_pb2.Etapa(etapa=3, turno="Noite")
        )

        vinculo = elegivel_pb2.Vinculo(
            id=1,
            matricula="2023113",
            tipo=elegivel_pb2.DISCENTE,
            id_pessoa=1,
            curso=curso
        )

        pessoa = elegivel_pb2.Pessoa(
            id=1,
            nome="João",
            cpf="12345678909",
            email="joao@example.com",
            data_nascimento="1998-12-01",
            vinculos=[vinculo]
        )

        elegivel = elegivel_pb2.Elegivel(
            pessoa=pessoa,
            foto_id=42
        )

        response = stub.EnviarElegivel(elegivel)
        print("Resposta do servidor:", response.mensagem)

if __name__ == '__main__':
    run()
