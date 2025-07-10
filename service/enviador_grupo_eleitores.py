import grpc
from eleitor.grpc import eleitor_pb2, eleitor_pb2_grpc



def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = eleitor_pb2_grpc.GrupoEleitorServiceStub(channel)

        curso1 = eleitor_pb2.Curso(
            id=1,
            nome="Curso A",
            descricao="Descrição do curso A",
            etapa=None
        )

        curso2 = eleitor_pb2.Curso(
            id=2,
            nome="Curso B",
            descricao="Descrição do curso B",
            etapa=None
        )

        vinculo1 = eleitor_pb2.Vinculo(
            id=1,
            matricula="1234567",
            tipo=1,
            id_pessoa=1,
            curso=curso1
        )

        vinculo2 = eleitor_pb2.Vinculo(
            id=2,
            matricula="7654321",
            tipo=2,
            id_pessoa=2,
            curso=curso2
        )

        pessoa1 = eleitor_pb2.Pessoa(
            id=1,
            nome="João",
            cpf="158.730.930-08",
            email="joao@example.com",
            data_nascimento="1990-01-01",
            vinculos=[vinculo1]
        )

        pessoa2 = eleitor_pb2.Pessoa(
            id=2,
            nome="Maria",
            cpf="158.730.930-08",
            email="maria@example.com",
            data_nascimento="1995-05-05",
            vinculos=[vinculo2]
        )

        eleitor1 = eleitor_pb2.Eleitor(
            pessoa=pessoa1,
            status=1
        )

        eleitor2 = eleitor_pb2.Eleitor(
            pessoa=pessoa2,
            status=2
        )

        grupo_request = eleitor_pb2.GrupoEleitores(
            id=1,
            nome="Grupo Teste",
            descricao="Teste do grupo com múltiplos eleitores",
            ativo=True,
            lista_eleitores=[eleitor1, eleitor2]  # lista com múltiplos eleitores
        )

        response = stub.EnviarGrupo(grupo_request)
        print("Resposta do servidor:", response.mensagem)


if __name__ == '__main__':
    run()
