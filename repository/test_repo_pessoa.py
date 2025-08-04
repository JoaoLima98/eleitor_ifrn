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

# Exemplo de classe Pessoa (ajuste conforme seu DTO ou modelo de entrada)

# Crie uma pessoa de teste
etapa_teste = Etapa(id=1,etapa=15, turno="Manhã")  # ajuste os valores conforme necessário
'''service_etapa = EtapaService()
etapa_salva = service_etapa.salvar(etapa_teste)'''
curso_teste = Curso(1 ,nome="Curso Teste2", descricao="Descrição do curso1", etapa=etapa_teste)
'''service_curso = CursoService()
service_curso.salvar(curso_teste)'''

vinculos_teste = [
    Vinculo(id=3, matricula="12345678901231", tipo=2, id_pessoa=1, curso=curso_teste),
]
'''
service_vinculo = VinculoService()
service_vinculo.salvar(vinculos_teste)'''
pessoa_teste = Pessoa(
    id=1,
    cpf="89097712084",
    email="fulano@teste.com",
    data_nascimento=date(2000, 1, 1),
    nome="Fulano Teste",
    vinculos= []
)
'''service_pessoa = PessoaService()
pessoa_teste = service_pessoa.salvar(pessoa_teste)'''

eleitor_teste = Eleitor(
    id=pessoa_teste.id,
    nome=pessoa_teste.nome,
    cpf=pessoa_teste.cpf,
    email=pessoa_teste.email,
    data_nascimento=pessoa_teste.data_nascimento,
    status=Status.ATIVO,  # ex.
    vinculos=pessoa_teste.vinculos
)

'''service_eleitor = EleitorService()
service_eleitor.salvar(eleitor_teste)'''

grupo_teste = GrupoEleitores(
    id=1,
    nome="Gru4po Jogoa2",
    descricao="Descrição do grupo de teste42",
    ativo=True,
    lista_eleitores=[eleitor_teste]
)
'''service_grupo = GrupoEleitoresService()
service_grupo.salvar(grupo_teste)
service_grupo.adicionar_eleitor(grupo_teste.id, eleitor_teste.id)'''