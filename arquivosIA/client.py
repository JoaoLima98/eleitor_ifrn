import sys
import os
import grpc
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar os arquivos gerados pelo protobuf
import gr.sysele_pb2 as sysEleitores
import gr.sysele_pb2_grpc as sysEleitoresgRPC


class SistemaVotacaoClient:
    """
    Cliente gRPC para o Sistema de Votação.
    Fornece métodos para testar todos os serviços disponíveis.
    """
    
    def __init__(self, host='localhost', port=8000):
        """
        Inicializa o cliente gRPC.
        
        Args:
            host (str): Endereço do servidor gRPC
            port (int): Porta do servidor gRPC
        """
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None
        self.conectar()
    
    def conectar(self):
        """Estabelece conexão com o servidor gRPC."""
        try:
            self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
            self.stub = sysEleitoresgRPC.SistemaVotacaoServiceStub(self.channel)
            print(f"Conectado ao servidor gRPC em {self.host}:{self.port}")
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {str(e)}")
            raise
    
    def desconectar(self):
        """Fecha a conexão com o servidor gRPC."""
        if self.channel:
            self.channel.close()
            print("Conexão com o servidor encerrada")
    
    def imprimir_cabecalho(self, titulo):
        """Imprime um cabeçalho formatado para os testes."""
        print("\n" + "=" * 60)
        print(f"=== {titulo} ===")
        print("=" * 60)
    
    def imprimir_rodape(self):
        """Imprime um rodapé formatado para os testes."""
        print("=" * 60)
    
    def tratar_erro(self, erro, contexto=""):
        """
        Trata erros de comunicação gRPC e outros erros.
        
        Args:
            erro: Exception capturada
            contexto (str): Contexto onde ocorreu o erro
        """
        if isinstance(erro, grpc.RpcError):
            print(f"Erro de comunicação gRPC em {contexto}: {erro.code()}: {erro.details()}")
        else:
            print(f"Erro inesperado em {contexto}: {str(erro)}")
    
    # Métodos para Etapa
    def testar_etapa(self):
        """
        Testa todos os métodos do serviço de Etapa.
        
        Returns:
            int: ID da etapa criada
        """
        self.imprimir_cabecalho("Testando Serviço de Etapa")
        
        try:
            # Salvar uma nova etapa
            etapa_request = sysEleitores.SalvarEtapaRequest(
                etapa=sysEleitores.Etapa(
                    id=0,  # ID será gerado pelo banco
                    etapa=1,
                    turno="Manhã"
                )
            )
            etapa_response = self.stub.SalvarEtapa(etapa_request)
            print(f"Etapa salva: ID={etapa_response.etapa.id}, Etapa={etapa_response.etapa.etapa}, Turno={etapa_response.etapa.turno}")
            etapa_id = etapa_response.etapa.id
            
            # Buscar etapa por ID
            buscar_request = sysEleitores.BuscarEtapaPorIdRequest(etapa_id=etapa_id)
            buscar_response = self.stub.BuscarEtapaPorId(buscar_request)
            print(f"Etapa encontrada: ID={buscar_response.etapa.id}, Etapa={buscar_response.etapa.etapa}, Turno={buscar_response.etapa.turno}")
            
            # Atualizar etapa
            atualizar_request = sysEleitores.AtualizarEtapaRequest(
                etapa_id=etapa_id,
                etapa=sysEleitores.Etapa(
                    etapa=2,
                    turno="Tarde"
                )
            )
            atualizar_response = self.stub.AtualizarEtapa(atualizar_request)
            print(f"Etapa atualizada: Sucesso={atualizar_response.sucesso}")
            
            # Remover etapa (comentado para não afetar o teste de curso)
            # remover_request = sysEleitores.RemoverEtapaRequest(etapa_id=etapa_id)
            # remover_response = self.stub.RemoverEtapa(remover_request)
            # print(f"Etapa removida: Sucesso={remover_response.sucesso}")
            
            self.imprimir_rodape()
            return etapa_id
            
        except Exception as e:
            self.tratar_erro(e, "teste de etapa")
            return None
    
    # Métodos para Curso
    def testar_curso(self, etapa_id):
        """
        Testa todos os métodos do serviço de Curso.
        
        Args:
            etapa_id (int): ID da etapa associada ao curso
            
        Returns:
            int: ID do curso criado
        """
        self.imprimir_cabecalho("Testando Serviço de Curso")
        
        try:
            # Buscar a etapa para garantir que ela existe
            buscar_etapa_request = sysEleitores.BuscarEtapaPorIdRequest(etapa_id=etapa_id)
            print(buscar_etapa_request, "Aqui asijfiasifjajfiajifaij")
            buscar_etapa_response = self.stub.BuscarEtapaPorId(buscar_etapa_request)
            print(f"Etapa encontrada para o curso: ID={buscar_etapa_response.etapa.id}, Etapa={buscar_etapa_response.etapa.etapa}, Turno={buscar_etapa_response.etapa.turno}")
            
            # Salvar um novo curso
            curso_request = sysEleitores.SalvarCursoRequest(
                curso=sysEleitores.Curso(
                    id=0,  # ID será gerado pelo banco
                    nome="Engenharia de Software",
                    descricao="Curso de graduação em Engenharia de Software",
                    etapa=buscar_etapa_response.etapa  # Incluir o objeto etapa completo
                )
            )
            curso_response = self.stub.SalvarCurso(curso_request)
            print(f"Curso salvo: ID={curso_response.curso.id}, Nome={curso_response.curso.nome}")
            curso_id = curso_response.curso.id
            
            # Buscar curso por ID
            buscar_request = sysEleitores.BuscarCursoPorIdRequest(curso_id=curso_id)
            buscar_response = self.stub.BuscarCursoPorId(buscar_request)
            print(f"Curso encontrado: ID={buscar_response.curso.id}, Nome={buscar_response.curso.nome}")
            
            # Verificar se nome existe
            nome_request = sysEleitores.GetNomeByNomeRequest(nome="Engenharia de Software")
            nome_response = self.stub.GetNomeByNome(nome_request)
            print(f"Nome 'Engenharia de Software' existe: {nome_response.existe}")
            
            # Atualizar curso
            # atualizar_request = sysEleitores.AtualizarCursoRequest(
            #     curso_id=curso_id,
            #     curso=sysEleitores.Curso(
            #         nome="Engenharia de Software Atualizado",
            #         descricao="Descrição atualizada",
            #         etapa=buscar_etapa_response.etapa  # Incluir o objeto etapa completo
            #     )
            # )
            # atualizar_response = self.stub.AtualizarCurso(atualizar_request)
            # print(f"Curso atualizado: Sucesso={atualizar_response.sucesso}")
            
            # Remover curso
            # remover_request = sysEleitores.RemoverCursoRequest(curso_id=curso_id)
            # remover_response = self.stub.RemoverCurso(remover_request)
            # print(f"Curso removido: Sucesso={remover_response.sucesso}")
            
            self.imprimir_rodape()
            return curso_response.curso
            
        except Exception as e:
            self.tratar_erro(e, "teste de curso")
            return None
    
    # Métodos para Pessoa
    def testar_pessoa(self):
        """
        Testa todos os métodos do serviço de Pessoa.
        
        Returns:
            int: ID da pessoa criada
        """
        self.imprimir_cabecalho("Testando Serviço de Pessoa")
        
        try:
            # Salvar uma nova pessoa
            pessoa_request = sysEleitores.SalvarPessoaRequest(
                pessoa=sysEleitores.Pessoa(
                    id=1,  # ID será gerado pelo banco
                    cpf="61578630053",
                    email="joao.silva@example.com",
                    data_nascimento="1990-05-15",
                    nome="João Silva",
                    vinculos=[]
                    
                )
            )
            pessoa_response = self.stub.SalvarPessoa(pessoa_request)
            print(f"Pessoa salva: ID={pessoa_response.pessoa.id}, Nome={pessoa_response.pessoa.nome}")
            pessoa_id = pessoa_response.pessoa.id
            print(pessoa_id, "ASUIFHUAHSFHAFUHASUFH")
            
            # Buscar pessoa por CPF
            cpf_request = sysEleitores.BuscarPessoaPorCpfRequest(cpf="61578630053")
            cpf_response = self.stub.BuscarPessoaPorCpf(cpf_request)
            print(f"Pessoa encontrada por CPF: ID={cpf_response.pessoa.id}, Nome={cpf_response.pessoa.nome}")
            
            # Buscar pessoa por email
            email_request = sysEleitores.BuscarPessoaPorEmailRequest(email="joao.silva@example.com")
            email_response = self.stub.BuscarPessoaPorEmail(email_request)
            print(f"Pessoa encontrada por email: ID={email_response.pessoa.id}, Nome={email_response.pessoa.nome}")
            
            # Atualizar pessoa
            atualizar_request = sysEleitores.AtualizarPessoaRequest(
                pessoa_id=pessoa_id,
                pessoa=sysEleitores.Pessoa(                  
                    cpf="61578630053",
                    email="joao.silva.atualizado@example.com",
                    data_nascimento="1990-05-15",
                    nome="João Silva",
                    vinculos=[]
                )
            )
            # atualizar_response = self.stub.AtualizarPessoa(atualizar_request)
            # print(f"Pessoa atualizada: Sucesso={atualizar_response.sucesso}")
            
            # Remover pessoa
            # remover_request = sysEleitores.RemoverPessoaRequest(pessoa_id=pessoa_id)
            # remover_response = self.stub.RemoverPessoa(remover_request)
            # print(f"Pessoa removida: Sucesso={remover_response.sucesso}")
            
            self.imprimir_rodape()
            return pessoa_id
            
        except Exception as e:
            self.tratar_erro(e, "teste de pessoa")
            return None
    
    # Métodos para Vinculo
    def testar_vinculo(self, pessoa_id, curso):
        """
        Testa todos os métodos do serviço de Vínculo.
        
        Args:
            pessoa_id (int): ID da pessoa associada ao vínculo
            curso_id (int): ID do curso associado ao vínculo
            
        Returns:
            int: ID do vínculo criado
        """
        self.imprimir_cabecalho("Testando Serviço de Vínculo")
        
        try:
            # Salvar um novo vínculo
            vinculo_request = sysEleitores.SalvarVinculoRequest(
                vinculo=sysEleitores.Vinculo(
                    id=0,  # ID será gerado pelo banco
                    matricula="2023001",
                    tipo=1,
                    id_pessoa=pessoa_id,
                    curso=curso
                )
            )
            print(vinculo_request)
            vinculo_response = self.stub.SalvarVinculo(vinculo_request)
            print(f"Vínculo salvo: ID={vinculo_response.vinculo.id}, Matrícula={vinculo_response.vinculo.matricula}")
            vinculo_id = vinculo_response.vinculo.id
            
            # Buscar vínculo por ID
            buscar_request = sysEleitores.BuscarVinculoPorIdRequest(vinculo_id=vinculo_id)
            buscar_response = self.stub.BuscarVinculoPorId(buscar_request)
            print(f"Vínculo encontrado: ID={buscar_response.vinculo.id}, Matrícula={buscar_response.vinculo.matricula}")
            
            # Atualizar vínculo
            atualizar_request = sysEleitores.AtualizarVinculoRequest(
                vinculo_id=vinculo_id,
                vinculo=sysEleitores.Vinculo(
                    matricula="2023000",
                    tipo=0,
                    curso=curso,
                    id_pessoa=pessoa_id
                )
            )
            atualizar_response = self.stub.AtualizarVinculo(atualizar_request)
            print(f"Vínculo atualizado: Sucesso={atualizar_response.sucesso}")
            
            # Remover vínculo
            remover_request = sysEleitores.RemoverVinculoRequest(vinculo_id=vinculo_id)
            remover_response = self.stub.RemoverVinculo(remover_request)
            print(f"Vínculo removido: Sucesso={remover_response.sucesso}")
            
            self.imprimir_rodape()
            return vinculo_id
            
        except Exception as e:
            self.tratar_erro(e, "teste de vínculo")
            return None
    
    # Métodos para Eleitor
    def testar_eleitor(self, pessoa_id):
        """
        Testa todos os métodos do serviço de Eleitor.
        
        Args:
            pessoa_id (int): ID da pessoa associada ao eleitor
            
        Returns:
            int: ID do eleitor criado
        """
        self.imprimir_cabecalho("Testando Serviço de Eleitor")
        
        try:
            # Salvar um novo eleitor
            eleitor_request = sysEleitores.SalvarEleitorRequest(
                eleitor=sysEleitores.Eleitor(
                    id=pessoa_id,  # ID da pessoa
                    nome="João Silva",
                    email="joao.silva@example.com",
                    cpf="61578630053",
                    data_nascimento="1990-05-15",
                    status=sysEleitores.StatusEnum.ATIVO
                )
            )
            eleitor_response = self.stub.SalvarEleitor(eleitor_request)
            print(f"Eleitor salvo: ID={eleitor_response.eleitor.id}, Status={eleitor_response.eleitor.status}")
            eleitor_id = eleitor_response.eleitor.id
            
            # Atualizar eleitor
            atualizar_request = sysEleitores.AtualizarEleitorRequest(
                eleitor_id=eleitor_id,
                eleitor=sysEleitores.Eleitor(
                    status=sysEleitores.StatusEnum.INATIVO
                )
            )
            atualizar_response = self.stub.AtualizarEleitor(atualizar_request)
            print(f"Eleitor atualizado: Sucesso={atualizar_response.sucesso}")
            
            # Remover eleitor
            remover_request = sysEleitores.RemoverEleitorRequest(eleitor_id=eleitor_id)
            remover_response = self.stub.RemoverEleitor(remover_request)
            print(f"Eleitor removido: Sucesso={remover_response.sucesso}")
            
            self.imprimir_rodape()
            return eleitor_id
            
        except Exception as e:
            self.tratar_erro(e, "teste de eleitor")
            return None
    
    # Métodos para GrupoEleitores
    def testar_grupo_eleitores(self, eleitor_id):
        """
        Testa todos os métodos do serviço de Grupo de Eleitores.
        
        Args:
            eleitor_id (int): ID do eleitor a ser adicionado ao grupo
            
        Returns:
            int: ID do grupo criado
        """
        self.imprimir_cabecalho("Testando Serviço de Grupo de Eleitores")
        
        try:
            # Salvar um novo grupo
            grupo_request = sysEleitores.SalvarGrupoRequest(
                grupo=sysEleitores.GrupoEleitores(
                    id=0,  # ID será gerado pelo banco
                    nome="Grupo de Teste",
                    descricao="Grupo criado para testes",
                    ativo=True
                )
            )
            grupo_response = self.stub.SalvarGrupo(grupo_request)
            print(f"Grupo salvo: ID={grupo_response.grupo.id}, Nome={grupo_response.grupo.nome}")
            grupo_id = grupo_response.grupo.id
            
            # Buscar grupo por ID
            buscar_id_request = sysEleitores.BuscarGrupoPorIdRequest(grupo_id=grupo_id)
            buscar_id_response = self.stub.BuscarGrupoPorId(buscar_id_request)
            print(f"Grupo encontrado por ID: ID={buscar_id_response.grupo.id}, Nome={buscar_id_response.grupo.nome}")
            
            # Buscar grupo por nome
            buscar_nome_request = sysEleitores.BuscarGrupoPorNomeRequest(nome="Grupo de Teste")
            buscar_nome_response = self.stub.BuscarGrupoPorNome(buscar_nome_request)
            print(f"Grupo encontrado por nome: ID={buscar_nome_response.grupo.id}, Nome={buscar_nome_response.grupo.nome}")
            
            # Adicionar eleitor ao grupo
            adicionar_request = sysEleitores.AdicionarEleitorRequest(
                grupo_id=grupo_id,
                eleitor_id=eleitor_id
            )
            adicionar_response = self.stub.AdicionarEleitor(adicionar_request)
            print(f"Eleitor adicionado ao grupo: Grupo ID={adicionar_response.grupo.id}, Eleitores={len(adicionar_response.grupo.eleitores)}")
            
            # Listar eleitores do grupo
            listar_request = sysEleitores.ListarEleitoresPorGrupoRequest(grupo_id=grupo_id)
            listar_response = self.stub.ListarEleitoresPorGrupo(listar_request)
            print(f"Eleitores no grupo: {len(listar_response.eleitores)}")
            for eleitor in listar_response.eleitores:
                print(f"  - ID: {eleitor.id}, Nome: {eleitor.nome}, Status: {eleitor.status}")
            
            # Ativar/Inativar grupo
            ativa_inativa_request = sysEleitores.AtivaInativaGrupoRequest(grupo_id=grupo_id)
            ativa_inativa_response = self.stub.AtivaInativaGrupo(ativa_inativa_request)
            print(f"Status do grupo alterado: Ativo={ativa_inativa_response.ativo}")
            
            # Remover eleitor do grupo
            remover_eleitor_request = sysEleitores.RemoverEleitorDoGrupoRequest(
                grupo_id=grupo_id,
                eleitor_id=eleitor_id
            )
            remover_eleitor_response = self.stub.RemoverEleitorDoGrupo(remover_eleitor_request)
            print(f"Eleitor removido do grupo: Grupo ID={remover_eleitor_response.grupo.id}, Eleitores={len(remover_eleitor_response.grupo.eleitores)}")
            
            # Listar todos os grupos
            listar_todos_request = sysEleitores.ListarTodosGruposRequest()
            listar_todos_response = self.stub.ListarTodosGrupos(listar_todos_request)
            print(f"Total de grupos: {len(listar_todos_response.grupos)}")
            for grupo in listar_todos_response.grupos:
                print(f"  - ID: {grupo.id}, Nome: {grupo.nome}, Ativo: {grupo.ativo}")
            
            # Atualizar grupo
            atualizar_request = sysEleitores.AtualizarGrupoRequest(
                grupo_id=grupo_id,
                grupo=sysEleitores.GrupoEleitores(
                    nome="Grupo de Teste Atualizado",
                    descricao="Descrição atualizada",
                    ativo=True
                )
            )
            atualizar_response = self.stub.AtualizarGrupo(atualizar_request)
            print(f"Grupo atualizado: Sucesso={atualizar_response.sucesso}")
            
            # Remover grupo
            remover_request = sysEleitores.RemoverGrupoRequest(grupo_id=grupo_id)
            remover_response = self.stub.RemoverGrupo(remover_request)
            print(f"Grupo removido: Sucesso={remover_response.sucesso}")
            
            self.imprimir_rodape()
            return grupo_id
            
        except Exception as e:
            self.tratar_erro(e, "teste de grupo de eleitores")
            return None
    
    def executar_todos_os_testes(self):
        """
        Executa todos os testes dos serviços em sequência.
        """
        print("Iniciando testes completos do Sistema de Votação via gRPC")
        print("=" * 60)
        
        try:
            # Testar Etapa
            etapa_id = self.testar_etapa()
            if etapa_id is None:
                print("Não foi possível criar uma etapa. Abortando testes.")
                return
            
            # Testar Curso (depende de uma etapa existente)
            curso_id = self.testar_curso(etapa_id=etapa_id)
            if curso_id is None:
                print("Não foi possível criar um curso. Abortando testes.")
                return
            
            # Testar Pessoa
            pessoa_id = self.testar_pessoa()
            if pessoa_id is None:
                print("Não foi possível criar uma pessoa. Abortando testes.")
                return
            
            # Testar Vínculo (depende de pessoa e curso)
            vinculo_id = self.testar_vinculo(pessoa_id, curso_id)
            if vinculo_id is None:
                print("Não foi possível criar um vínculo. Continuando com os próximos testes.")
            
            # Testar Eleitor (depende de pessoa)
            eleitor_id = self.testar_eleitor(pessoa_id)
            if eleitor_id is None:
                print("Não foi possível criar um eleitor. Abortando testes.")
                return
            
            # Testar Grupo de Eleitores (depende de eleitor)
            grupo_id = self.testar_grupo_eleitores(eleitor_id)
            if grupo_id is None:
                print("Não foi possível criar um grupo de eleitores.")
            
            print("\n" + "=" * 60)
            print("Todos os testes foram concluídos!")
            print("=" * 60)
            
        except Exception as e:
            self.tratar_erro(e, "execução dos testes")
        finally:
            self.desconectar()
    
    def executar_teste_especifico(self, servico):
        """
        Executa um teste específico baseado no nome do serviço.
        
        Args:
            servico (str): Nome do serviço a ser testado (etapa, curso, pessoa, vinculo, eleitor, grupo)
        """
        servico = servico.lower()
        
        if servico == "etapa":
            self.testar_etapa()
        elif servico == "curso":
            # Para testar curso, precisamos de uma etapa
            etapa_id = self.testar_etapa()
            if etapa_id:
                self.testar_curso(etapa_id)
        elif servico == "pessoa":
            self.testar_pessoa()
        elif servico == "vinculo":
            # Para testar vinculo, precisamos de pessoa e curso
            pessoa_id = self.testar_pessoa()
            if pessoa_id:
                etapa_id = self.testar_etapa()
                if etapa_id:
                    curso_id = self.testar_curso(etapa_id)
                    if curso_id:
                        self.testar_vinculo(pessoa_id, curso_id)
        elif servico == "eleitor":
            # Para testar eleitor, precisamos de pessoa
            pessoa_id = self.testar_pessoa()
            if pessoa_id:
                self.testar_eleitor(pessoa_id)
        elif servico == "grupo":
            # Para testar grupo, precisamos de eleitor
            pessoa_id = self.testar_pessoa()
            if pessoa_id:
                eleitor_id = self.testar_eleitor(pessoa_id)
                if eleitor_id:
                    self.testar_grupo_eleitores(eleitor_id)
        else:
            print(f"Serviço '{servico}' não reconhecido. Opções válidas: etapa, curso, pessoa, vinculo, eleitor, grupo")
        
        self.desconectar()

if __name__ == '__main__':
    import argparse
    
    # Configurar o parser de argumentos
    parser = argparse.ArgumentParser(description='Cliente gRPC para testar o Sistema de Votação')
    parser.add_argument('--host', default='localhost', help='Endereço do servidor gRPC (default: localhost)')
    parser.add_argument('--port', type=int, default=8000, help='Porta do servidor gRPC (default: 8000)')
    parser.add_argument('--servico', choices=['etapa', 'curso', 'pessoa', 'vinculo', 'eleitor', 'grupo', 'todos'], 
                        default='todos', help='Serviço a ser testado (default: todos)')
    
    args = parser.parse_args()
    
    # Configurar o cliente
    client = SistemaVotacaoClient(host=args.host, port=args.port)
    
    try:
        # Executar o teste selecionado
        if args.servico == 'todos':
            client.executar_todos_os_testes()
        else:
            client.executar_teste_especifico(args.servico)
    except KeyboardInterrupt:
        print("\nTestes interrompidos pelo usuário.")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
    finally:
        client.desconectar()