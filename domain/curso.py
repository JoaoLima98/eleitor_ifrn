from domain.etapa import Etapa

class Curso:
    
    def __init__(self,id: int, nome:str, descricao: str, etapa: Etapa = None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.etapa = etapa
        self.descricao_nao_e_falsy()
        self.nome_nao_e_falsy()
        
    def definir_etapa(self, etapa: Etapa):
        self.etapa = etapa
        return self.etapa

    def descricao_nao_e_falsy(self):
        if not bool(self.descricao):
            raise ValueError("Descrição inválida.")
        return True
    def nome_nao_e_falsy(self):
        if not bool(self.nome):
            raise ValueError("Nome inválido.")
        return True