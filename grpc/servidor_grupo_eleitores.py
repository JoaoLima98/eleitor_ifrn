from eleitor.domain.curso import Curso
from eleitor.domain.vinculo import Vinculo
from eleitor.domain.pessoa import Pessoa
from eleitor.domain.eleitor import Eleitor
from eleitor.domain.grupo_eleitores import GrupoEleitores
import grpc
from eleitor.grpc import eleitor_pb2, eleitor_pb2_grpc
from concurrent import futures
from datetime import datetime

def convert_str_to_date(data_str: str):
    return datetime.strptime(data_str, "%Y-%m-%d").date()

class GrupoEleitorServiceImpl(eleitor_pb2_grpc.GrupoEleitorServiceServicer):
    def EnviarGrupo(self, request, context):
        try:
            lista_eleitores_dominio = []
            for eleitor_proto in request.lista_eleitores:
                vinculos = []
                for v_proto in eleitor_proto.pessoa.vinculos:
                    curso = Curso(
                        id=v_proto.curso.id,
                        nome=v_proto.curso.nome,
                        descricao=v_proto.curso.descricao,
                        etapa=None
                    )
                    vinculo = Vinculo(
                        id=v_proto.id,
                        matricula=v_proto.matricula,
                        tipo=v_proto.tipo,
                        id_pessoa=v_proto.id_pessoa,
                        curso=curso
                    )
                    vinculos.append(vinculo)

                eleitor = Eleitor(
                    id=eleitor_proto.pessoa.id,
                    nome=eleitor_proto.pessoa.nome,
                    email=eleitor_proto.pessoa.email,
                    cpf=eleitor_proto.pessoa.cpf,
                    data_nascimento=convert_str_to_date(eleitor_proto.pessoa.data_nascimento),
                    status=eleitor_proto.status,
                    vinculos=vinculos
                )
                lista_eleitores_dominio.append(eleitor)

                print(f"Eleitor: {eleitor.nome} - CPF: {eleitor.cpf} - Data Nasc: {eleitor.data_nascimento}")
                for v in vinculos:
                        print(f"  Vínculo: Matrícula: {v.matricula}, Tipo: {v.tipo}, Curso: {v.curso.nome}")


            grupo = GrupoEleitores(
                id=request.id,
                nome=request.nome,
                descricao=request.descricao,
                ativo=request.ativo
            )
            grupo.set_lista_eleitores(lista_eleitores_dominio)  # usa o método para setar a lista

            print(f"Grupo {grupo.nome} com {len(grupo.get_lista_eleitores())} eleitores recebido e validado.")

            return eleitor_pb2.EnviarGrupoResponse(mensagem="Grupo recebido e validado com sucesso")

        except Exception as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    eleitor_pb2_grpc.add_GrupoEleitorServiceServicer_to_server(
        GrupoEleitorServiceImpl(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC escutando na porta 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
