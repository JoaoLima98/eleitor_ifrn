from eleitor.domain.etapa import Etapa
from eleitor.service.curso_service import CursoService

class Curso:
    
    def __init__(self,id: int, nome:str, descricao: str, etapa: Etapa = None, service: CursoService = CursoService()):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.etapa = etapa
        self.descricao_nao_e_falsy()
        self.nome_nao_e_falsy()
        self.service = service
        self.verifica_nome_unico()
        
    def definir_etapa(self, etapa: Etapa):
        self.etapa = etapa
        return self.etapa
        
    def verifica_nome_unico(self):
        if not self.service.get_nome_by_nome(self.nome):
            raise ValueError("Nome já cadastrado.")
        return self.nome

    def descricao_nao_e_falsy(self):
        if not bool(self.descricao):
            raise ValueError("Descrição inválida.")
        return True
    def nome_nao_e_falsy(self):
        if not bool(self.nome):
            raise ValueError("Nome inválido.")
        return True