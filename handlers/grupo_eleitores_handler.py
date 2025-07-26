import grupo_eleitores_pb2
import grupo_eleitores_pb2_grpc

class GrupoEleitoresGrpcHandler(grupo_eleitores_pb2_grpc.GrupoEleitoresServiceServicer):
    def __init__(self, grupo_service):
        self.grupo_service = grupo_service

    def EnviarGrupo(self, request, context):
        grupo = self.grupo_service.buscar_por_id(request.id)
        if not grupo:
            context.abort(5, "Grupo não encontrado")  # StatusCode.NOT_FOUND

        return self._grupo_to_grpc(grupo)

    def _grupo_to_grpc(self, grupo):
        return grupo_eleitores_pb2.GrupoEleitoresMessage(
            id=grupo.id,
            nome=grupo.nome,
            descricao=grupo.descricao,
            ativo=grupo.ativo,
            data_cadastro=grupo.data_cadastro.isoformat(),
            data_atualizacao=grupo.data_atualizacao.isoformat(),
            lista_eleitores=[
                grupo_eleitores_pb2.EleitorMessage(
                    id=e.id,
                    nome=e.nome,
                    email=e.email,
                    cpf=e.cpf,
                    data_nascimento=e.data_nascimento.isoformat(),
                    status=e.status.name
                ) for e in grupo.get_lista_eleitores()
            ]
        )
