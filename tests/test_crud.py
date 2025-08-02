
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from service.pessoa_service import PessoaService
from service.etapa_service import EtapaService
from service.curso_service import CursoService
from service.vinculo_service import VinculoService
from service.eleitor_service import EleitorService
from service.grupo_eleitores_service import GrupoEleitoresService
from domain.eleitor import Eleitor
from domain.enum.status import Status
from domain.grupo_eleitores import GrupoEleitores
from models import models  
from datetime import date
from domain.pessoa import Pessoa  
from domain.vinculo import Vinculo  
from domain.curso import Curso  
from domain.etapa import Etapa
from domain.enum.tipo_vinculo import TipoVinculo



etapa_teste = Etapa(id=3,etapa=15, turno="Manhã")  # ajuste os valores conforme necessário
service_etapa = EtapaService()
'''service_etapa.salvar(etapa_teste)'''
curso_teste = Curso(3 ,nome="Curso Teste2", descricao="Descrição do curso1", etapa=etapa_teste)
service_curso = CursoService()
'''service_curso.salvar(curso_teste)'''

service_vinculo = VinculoService()

pessoa_teste = Pessoa(id=1,
    cpf="89097712084",
    email="fulano@teste2.com",
    data_nascimento=date(2000, 1, 1),
    nome="Fulano Teste",
    vinculos= [])

testevinculo = Vinculo(id=3, matricula="12345678901235", tipo=TipoVinculo.DISCENTE, id_pessoa=1, curso=curso_teste)

'''service_vinculo.remover(1)'''

pessoa_service = PessoaService()

'''pessoa_service.salvar(pessoa)'''
eleitor_service = EleitorService()
eleitor = Eleitor(id=pessoa_teste.id,
    nome=pessoa_teste.nome,
    cpf=pessoa_teste.cpf,
    email=pessoa_teste.email,
    data_nascimento=pessoa_teste.data_nascimento,
    status=Status.SUSPENSO,  # ex.
    vinculos=pessoa_teste.vinculos)

print(eleitor.nome + "dddddddddddddddddddddddddddd")

'''eleitor_service.atualizar(eleitor, 1)'''

grupo2 = GrupoEleitores(1, "nome_grupo2", "descricao", True, eleitor)

grupo_service = GrupoEleitoresService()

print(grupo_service.listar_todos_os_grupos())