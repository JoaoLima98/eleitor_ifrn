from typing import List
from unittest.mock import patch
from domain.eleitor import Eleitor
from datetime import datetime

class GrupoEleitores:
    
    def __init__(self, id: int,  nome: str, descricao: str, ativo: bool = True, lista_eleitores: List[Eleitor] = []):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.ativo = ativo
        self.lista_eleitores: List[Eleitor] = lista_eleitores
        self.data_cadastro = datetime.now()
        self.data_atualizacao = datetime.now()
        self.verifica_se_nome_nao_e_falsy()
    
    

    def verifica_se_nome_nao_e_falsy(self):
        if not bool(self.nome):
            raise ValueError("Nome inválido.")
        return True
    
    
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