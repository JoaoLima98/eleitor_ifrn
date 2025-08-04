import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import grpc
from concurrent import futures
from gr import sysele_pb2
from gr import sysele_pb2_grpc

# Importar todos os serviços
from service.etapa_service import EtapaService
from service.curso_service import CursoService
from service.pessoa_service import PessoaService
from service.vinculo_service import VinculoService
from service.eleitor_service import EleitorService
from service.grupo_eleitores_service import GrupoEleitoresService

# Importar domínios
from domain.etapa import Etapa
from domain.curso import Curso
from domain.pessoa import Pessoa
from domain.vinculo import Vinculo
from domain.eleitor import Eleitor
from domain.grupo_eleitores import GrupoEleitores
from domain.enum.tipo_vinculo import TipoVinculo
from domain.enum.status import Status

from datetime import datetime

class SistemaVotacaoServicer(sysele_pb2_grpc.SistemaVotacaoServiceServicer):
    def __init__(self):
        self.etapa_service = EtapaService()
        self.curso_service = CursoService()
        self.pessoa_service = PessoaService()
        self.vinculo_service = VinculoService()
        self.eleitor_service = EleitorService()
        self.grupo_eleitores_service = GrupoEleitoresService()

    # Conversores

    def converter_etapa_domain_to_pb(self, etapa: Etapa):
        return sysele_pb2.Etapa(
            id=etapa.id,
            etapa=etapa.etapa,
            turno=etapa.turno
        )

    def converter_etapa_pb_to_domain(self, etapa_pb):
        return Etapa(
            id=etapa_pb.id,
            etapa=etapa_pb.etapa,
            turno=etapa_pb.turno
        )

    def converter_curso_domain_to_pb(self, curso: Curso):
        etapa_pb = self.converter_etapa_domain_to_pb(curso.etapa)
        return sysele_pb2.Curso(
            id=curso.id,
            nome=curso.nome,
            descricao=curso.descricao,
            etapa=etapa_pb
        )

    def converter_curso_pb_to_domain(self, curso_pb):
        etapa_domain = self.converter_etapa_pb_to_domain(curso_pb.etapa)
        return Curso(
            id=curso_pb.id,
            nome=curso_pb.nome,
            descricao=curso_pb.descricao,
            etapa=etapa_domain
        )

    def converter_pessoa_domain_to_pb(self, pessoa: Pessoa):
        return sysele_pb2.Pessoa(
            id=pessoa.id,
            cpf=pessoa.cpf,
            email=pessoa.email,
            data_nascimento=pessoa.data_nascimento,
            nome=pessoa.nome,
            vinculos=[]
        )

    def converter_pessoa_pb_to_domain(self, pessoa_pb):
        return Pessoa(
            id=pessoa_pb.id,
            cpf=pessoa_pb.cpf,
            email=pessoa_pb.email,
            data_nascimento=pessoa_pb.data_nascimento,
            nome=pessoa_pb.nome,
            vinculos=[]
        )

    def converter_vinculo_domain_to_pb(self, vinculo: Vinculo):
        curso_pb = self.converter_curso_domain_to_pb(vinculo.curso)
        tipo = TipoVinculo.DISCENTE if vinculo.tipo == sysele_pb2.TipoVinculo.DISCENTE else TipoVinculo.DOCENTE
        return Vinculo(
            id=vinculo.id,
            matricula=vinculo.matricula,
            tipo=tipo,
            id_pessoa=vinculo.id_pessoa,
            curso=curso_pb
        )


    def converter_vinculo_pb_to_domain(self, vinculo_pb):
        curso = self.converter_curso_pb_to_domain(vinculo_pb.curso)
        tipo = TipoVinculo.DISCENTE if vinculo_pb.tipo == sysele_pb2.TipoVinculo.DISCENTE else TipoVinculo.DOCENTE
        return Vinculo(
            id=vinculo_pb.id,
            matricula=vinculo_pb.matricula,
            tipo=tipo,
            id_pessoa=vinculo_pb.id_pessoa,
            curso=curso
        )


    def converter_eleitor_domain_to_pb(self, eleitor: Eleitor):
        status = {
            Status.ATIVO: sysele_pb2.StatusEnum.ATIVO,
            Status.INATIVO: sysele_pb2.StatusEnum.INATIVO,
            Status.SUSPENSO: sysele_pb2.StatusEnum.SUSPENSO
        }.get(eleitor.status, sysele_pb2.StatusEnum.ATIVO)
        data = eleitor.data_nascimento.strftime("%Y-%m-%d") if eleitor.data_nascimento else ""
        return sysele_pb2.Eleitor(
            id=eleitor.id,
            nome=eleitor.nome,
            email=eleitor.email,
            cpf=eleitor.cpf,
            data_nascimento=data,
            status=status
        )

    def converter_eleitor_pb_to_domain(self, eleitor_pb):
        status = {
            sysele_pb2.StatusEnum.ATIVO: Status.ATIVO,
            sysele_pb2.StatusEnum.INATIVO: Status.INATIVO,
            sysele_pb2.StatusEnum.SUSPENSO: Status.SUSPENSO
        }.get(eleitor_pb.status, Status.ATIVO)

        return Eleitor(
            id=eleitor_pb.id,
            nome=eleitor_pb.nome,
            email=eleitor_pb.email,
            cpf=eleitor_pb.cpf,
            data_nascimento=eleitor_pb.data_nascimento,
            status=status
        )

    def converter_grupo_domain_to_pb(self, grupo: GrupoEleitores):
        eleitores_pb = [self.converter_eleitor_domain_to_pb(e) for e in (grupo.lista_eleitores or [])]
        return sysele_pb2.GrupoEleitores(
            id=grupo.id,
            nome=grupo.nome,
            descricao=grupo.descricao,
            ativo=grupo.ativo,
            eleitores=eleitores_pb
        )

    def converter_grupo_pb_to_domain(self, grupo_pb):
        eleitores = [self.converter_eleitor_pb_to_domain(e) for e in grupo_pb.eleitores]
        return GrupoEleitores(
            id=grupo_pb.id,
            nome=grupo_pb.nome,
            descricao=grupo_pb.descricao,
            ativo=grupo_pb.ativo,
            lista_eleitores=eleitores
        )

    # Implementações dos métodos gRPC

    # --- Etapa ---
    def SalvarEtapa(self, request, context):
        try:
            domain = self.converter_etapa_pb_to_domain(request.etapa)
            salvo = self.etapa_service.salvar(domain)
            return sysele_pb2.SalvarEtapaResponse(etapa=self.converter_etapa_domain_to_pb(salvo))
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return sysele_pb2.SalvarEtapaResponse()

    def BuscarEtapaPorId(self, request, context):
        etapa = self.etapa_service.buscar_por_id(request.etapa_id)
        if not etapa:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Etapa não encontrada")
            return sysele_pb2.BuscarEtapaPorIdResponse()
        return sysele_pb2.BuscarEtapaPorIdResponse(etapa=self.converter_etapa_domain_to_pb(etapa))

    def AtualizarEtapa(self, request, context):
        try:
            domain = self.converter_etapa_pb_to_domain(request.etapa)
            self.etapa_service.atualizar(domain, request.etapa_id)
            return sysele_pb2.AtualizarEtapaResponse(sucesso=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return sysele_pb2.AtualizarEtapaResponse(sucesso=False)

    def RemoverEtapa(self, request, context):
        try:
            self.etapa_service.remover(request.etapa_id)
            return sysele_pb2.RemoverEtapaResponse(sucesso=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return sysele_pb2.RemoverEtapaResponse(sucesso=False)

    # --- Curso ---
    def SalvarCurso(self, request, context):
        try:
            domain = self.converter_curso_pb_to_domain(request.curso)
            salvo = self.curso_service.salvar(domain)
            return sysele_pb2.SalvarCursoResponse(curso=self.converter_curso_domain_to_pb(salvo))
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return sysele_pb2.SalvarCursoResponse()

    def BuscarCursoPorId(self, request, context):
        curso = self.curso_service.buscar_por_id(request.curso_id)
        if not curso:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Curso não encontrado")
            return sysele_pb2.BuscarCursoPorIdResponse()
        return sysele_pb2.BuscarCursoPorIdResponse(curso=self.converter_curso_domain_to_pb(curso))

    def GetNomeByNome(self, request, context):
        try:
            existe = self.curso_service.get_nome_by_nome(request.nome)
            return sysele_pb2.GetNomeByNomeResponse(existe=existe)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return sysele_pb2.GetNomeByNomeResponse()

    def AtualizarCurso(self, request, context):
        try:
            domain = self.converter_curso_pb_to_domain(request.curso)
            self.curso_service.atualizar(domain, request.curso_id)
            return sysele_pb2.AtualizarCursoResponse(sucesso=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return sysele_pb2.AtualizarCursoResponse(sucesso=False)

    def RemoverCurso(self, request, context):
        try:
            self.curso_service.remover(request.curso_id)
            return sysele_pb2.RemoverCursoResponse(sucesso=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return sysele_pb2.RemoverCursoResponse(sucesso=False)

    # --- Pessoa ---
    def SalvarPessoa(self, request, context):
        try:
            domain = self.converter_pessoa_pb_to_domain(request.pessoa)
            salvo = self.pessoa_service.salvar(domain)
            return sysele_pb2.SalvarPessoaResponse(pessoa=self.converter_pessoa_domain_to_pb(salvo))
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return sysele_pb2.SalvarPessoaResponse()

    def BuscarPessoaPorCpf(self, request, context):
        try:
            pessoa = self.pessoa_service.buscar_por_cpf(request.cpf)
            if not pessoa:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Pessoa não encontrada")
                return sysele_pb2.BuscarPessoaPorCpfResponse()
            return sysele_pb2.BuscarPessoaPorCpfResponse(pessoa=self.converter_pessoa_domain_to_pb(pessoa))
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return sysele_pb2.BuscarPessoaPorCpfResponse()

    def BuscarPessoaPorEmail(self, request, context):
        try:
            pessoa = self.pessoa_service.buscar_por_email(request.email)
            if not pessoa:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Pessoa não encontrada")
                return sysele_pb2.BuscarPessoaPorEmailResponse()
            return sysele_pb2.BuscarPessoaPorEmailResponse(pessoa=self.converter_pessoa_domain_to_pb(pessoa))
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return sysele_pb2.BuscarPessoaPorEmailResponse()

    def AtualizarPessoa(self, request, context):
        try:
            domain = self.converter_pessoa_pb_to_domain(request.pessoa)
            self.pessoa_service.atualizar(domain, request.pessoa_id)
            return sysele_pb2.AtualizarPessoaResponse(sucesso=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return sysele_pb2.AtualizarPessoaResponse(sucesso=False)

    def RemoverPessoa(self, request, context):
        try:
            self.pessoa_service.remover(request.pessoa_id)
            return sysele_pb2.RemoverPessoaResponse(sucesso=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return sysele_pb2.RemoverPessoaResponse(sucesso=False)

    # --- Vinculo ---
    def SalvarVinculo(self, request, context):
        try:
            domain = self.converter_vinculo_pb_to_domain(request.vinculo)
            salvo = self.vinculo_service.salvar(domain)
            return sysele_pb2.SalvarVinculoResponse(vinculo=self.converter_vinculo_domain_to_pb(salvo))
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return sysele_pb2.SalvarVinculoResponse()

    def BuscarVinculoPorId(self, request, context):
        vinculo = self.vinculo_service.buscar_por_id(request.vinculo_id)
        if not vinculo:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Vínculo não encontrado")
            return sysele_pb2.BuscarVinculoPorIdResponse()
        return sysele_pb2.BuscarVinculoPorIdResponse(vinculo=self.converter_vinculo_domain_to_pb(vinculo))

    def AtualizarVinculo(self, request, context):
        try:
            domain = self.converter_vinculo_pb_to_domain(request.vinculo)
            self.vinculo_service.atualizar(domain, request.vinculo_id)
            return sysele_pb2.AtualizarVinculoResponse(sucesso=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return sysele_pb2.AtualizarVinculoResponse(sucesso=False)

    def RemoverVinculo(self, request, context):
        try:
            self.vinculo_service.remover(request.vinculo_id)
            return sysele_pb2.RemoverVinculoResponse(sucesso=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return sysele_pb2.RemoverVinculoResponse(sucesso=False)

    # --- Eleitor ---
    def SalvarEleitor(self, request, context):
        try:
            domain = self.converter_eleitor_pb_to_domain(request.eleitor)
            salvo = self.eleitor_service.salvar(domain)
            return sysele_pb2.SalvarEleitorResponse(eleitor=self.converter_eleitor_domain_to_pb(salvo))
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return sysele_pb2.SalvarEleitorResponse()

    def AtualizarEleitor(self, request, context):
        try:
            domain = self.converter_eleitor_pb_to_domain(request.eleitor)
            self.eleitor_service.atualizar(domain, request.eleitor_id)
            return sysele_pb2.AtualizarEleitorResponse(sucesso=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return sysele_pb2.AtualizarEleitorResponse(sucesso=False)

    def RemoverEleitor(self, request, context):
        try:
            self.eleitor_service.remover(request.eleitor_id)
            return sysele_pb2.RemoverEleitorResponse(sucesso=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return sysele_pb2.RemoverEleitorResponse(sucesso=False)

    # --- GrupoEleitores ---
    def SalvarGrupo(self, request, context):
        try:
            domain = self.converter_grupo_pb_to_domain(request.grupo)
            salvo = self.grupo_eleitores_service.salvar(domain)
            return sysele_pb2.SalvarGrupoResponse(grupo=self.converter_grupo_domain_to_pb(salvo))
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return sysele_pb2.SalvarGrupoResponse()

    def BuscarGrupoPorId(self, request, context):
        grupo = self.grupo_eleitores_service.buscar_por_id(request.grupo_id)
        if not grupo:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Grupo não encontrado")
            return sysele_pb2.BuscarGrupoPorIdResponse()
        return sysele_pb2.BuscarGrupoPorIdResponse(grupo=self.converter_grupo_domain_to_pb(grupo))

    def BuscarGrupoPorNome(self, request, context):
        grupo = self.grupo_eleitores_service.buscar_por_nome(request.nome)
        if not grupo:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Grupo não encontrado")
            return sysele_pb2.BuscarGrupoPorNomeResponse()
        return sysele_pb2.BuscarGrupoPorNomeResponse(grupo=self.converter_grupo_domain_to_pb(grupo))

    def AdicionarEleitor(self, request, context):
        try:
            eleitor = Eleitor(id=request.eleitor_id)
            grupo = self.grupo_eleitores_service.adicionar_eleitor(request.grupo_id, eleitor)
            return sysele_pb2.AdicionarEleitorResponse(grupo=self.converter_grupo_domain_to_pb(grupo))
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return sysele_pb2.AdicionarEleitorResponse()

    def RemoverEleitorDoGrupo(self, request, context):
        try:
            eleitor = Eleitor(id=request.eleitor_id)
            grupo = self.grupo_eleitores_service.remover_eleitor(request.grupo_id, eleitor)
            return sysele_pb2.RemoverEleitorDoGrupoResponse(grupo=self.converter_grupo_domain_to_pb(grupo))
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return sysele_pb2.RemoverEleitorDoGrupoResponse()

    def AtivaInativaGrupo(self, request, context):
        try:
            ativo = self.grupo_eleitores_service.ativa_inativa_grupo(request.grupo_id)
            return sysele_pb2.AtivaInativaGrupoResponse(ativo=ativo)
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return sysele_pb2.AtivaInativaGrupoResponse()

    def ListarEleitoresPorGrupo(self, request, context):
        try:
            eleitores = self.grupo_eleitores_service.listar_eleitores_por_grupo_id(request.grupo_id)
            eleitores_pb = [self.converter_eleitor_domain_to_pb(e) for e in eleitores]
            return sysele_pb2.ListarEleitoresPorGrupoResponse(eleitores=eleitores_pb)
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return sysele_pb2.ListarEleitoresPorGrupoResponse()

    def ListarTodosGrupos(self, request, context):
        grupos = self.grupo_eleitores_service.listar_todos_os_grupos()
        grupos_pb = [self.converter_grupo_domain_to_pb(g) for g in grupos]
        return sysele_pb2.ListarTodosGruposResponse(grupos=grupos_pb)

    def AtualizarGrupo(self, request, context):
        try:
            domain = self.converter_grupo_pb_to_domain(request.grupo)
            self.grupo_eleitores_service.atualizar(domain, request.grupo_id)
            return sysele_pb2.AtualizarGrupoResponse(sucesso=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return sysele_pb2.AtualizarGrupoResponse(sucesso=False)

    def RemoverGrupo(self, request, context):
        try:
            self.grupo_eleitores_service.remover(request.grupo_id)
            return sysele_pb2.RemoverGrupoResponse(sucesso=True)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return sysele_pb2.RemoverGrupoResponse(sucesso=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sysele_pb2_grpc.add_SistemaVotacaoServiceServicer_to_server(SistemaVotacaoServicer(), server)
    server.add_insecure_port('[::]:8000')
    server.start()
    print("Servidor gRPC iniciado na porta 8000")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()