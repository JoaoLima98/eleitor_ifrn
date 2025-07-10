from typing import List
from unittest.mock import patch
from eleitor.domain.eleitor import Eleitor
from datetime import datetime
from eleitor.service.grupo_eleitores_service import GrupoEleitoresService

class GrupoEleitores:
    
    def __init__(self, id: int,  nome: str, descricao: str, ativo: bool = True, service: GrupoEleitoresService = GrupoEleitoresService()):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.ativo = ativo
        self.lista_eleitores: List[Eleitor] = []
        self.data_cadastro = datetime.now()
        self.data_atualizacao = datetime.now()
        self.service = service
        self.verifica_se_nome_nao_e_falsy()
        self.verifica_nome_unico()
    
    

    def verifica_se_nome_nao_e_falsy(self):
        if not bool(self.nome):
            raise ValueError("Nome inválido.")
        return True
    
    def verifica_nome_unico(self):
        if not self.service.get_nome_by_nome(self.nome):
            raise ValueError("Nome já cadastrado.")
        return self.nome
    
    def set_lista_eleitores(self, lista: List[Eleitor]):
        self.lista_eleitores = lista
        return lista
    
    def append_lista_eleitores(self, eleitor: Eleitor):
        if eleitor in self.lista_eleitores:
            raise ValueError("Eleitor já está na lista.")
        
        self.lista_eleitores.append(eleitor)
        return eleitor
    
    def remove_eleitor_da_lista(self, eleitor: Eleitor):
        if eleitor not in self.lista_eleitores:
            raise ValueError("Eleitor não encontrado na lista.")
        
        self.lista_eleitores.remove(eleitor)
        return eleitor
            
    
    def get_lista_eleitores(self):
        return self.lista_eleitores
    
    def ativa_inativa_grupo(self):
        self.ativo = not self.ativo
        return self.ativo