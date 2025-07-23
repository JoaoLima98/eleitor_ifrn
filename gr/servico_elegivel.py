import grpc
from concurrent import futures
from grpc import elegivel_pb2, elegivel_pb2_grpc
from eleitor.domain.elegivel import Elegivel
from eleitor.domain.curso import Curso
from eleitor.domain.vinculo import Vinculo
from eleitor.domain.etapa import Etapa 
from datetime import datetime


def convert_str_to_date(data_str: str):
    return datetime.strptime(data_str, "%Y-%m-%d").date()


class ElegivelServiceImpl(elegivel_pb2_grpc.ElegivelServiceServicer):
    def EnviarElegivel(self, request, context):
        try:
            pessoa_proto = request.pessoa
            vinculos = []
            for v in pessoa_proto.vinculos:
                etapa = Etapa(
                    etapa=v.curso.etapa.etapa,
                    turno=v.curso.etapa.turno
                )
                curso = Curso(
                    id=v.curso.id,
                    nome=v.curso.nome,
                    descricao=v.curso.descricao,
                    etapa=etapa
                )
                vinculo = Vinculo(
                    id=v.id,
                    matricula=v.matricula,
                    tipo=v.tipo,
                    id_pessoa=v.id_pessoa,
                    curso=curso
                )
                vinculos.append(vinculo)

            elegivel_dominio = Elegivel(
                id=pessoa_proto.id,
                nome=pessoa_proto.nome,
                email=pessoa_proto.email,
                cpf=pessoa_proto.cpf,
                data_nascimento=convert_str_to_date(pessoa_proto.data_nascimento),
                foto_id=request.foto_id,
                vinculos=vinculos
            )

            print(f"Elegível recebido: {elegivel_dominio.nome} - CPF: {elegivel_dominio.cpf} - Foto ID: {elegivel_dominio.foto_id}")
            return elegivel_pb2.EnviarElegivelResponse(mensagem="Elegível recebido e validado com sucesso!")

        except Exception as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    elegivel_pb2_grpc.add_ElegivelServiceServicer_to_server(ElegivelServiceImpl(), server)
    server.add_insecure_port('[::]:8000')
    server.start()
    print("Servidor gRPC ouvindo na porta 8000...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
