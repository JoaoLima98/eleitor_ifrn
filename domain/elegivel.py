from domain.pessoa import Pessoa
from datetime import date, datetime

from domain.vinculo import Vinculo

class Elegivel(Pessoa):
    def __init__(self, id: int, nome: str, email: str, cpf: str, data_nascimento: date, foto_id: int, vinculos: list[Vinculo]):
        super().__init__(
            id=id,
            cpf=cpf,
            email=email,
            data_nascimento=data_nascimento,
            nome=nome,
            vinculos=vinculos
        )
        self.id = id
        self.adicionar_foto(foto_id)
        self.data_cadastro = datetime.now() 
        self.data_atualizacao = datetime.now()
        self.verifica_se_foto_nao_e_falsy()
        
    def verifica_se_foto_nao_e_falsy(self):
        if not bool(self.foto_id):
            raise ValueError("Foto inválida.")
        return True
        
    def adicionar_foto(self, foto_id: int):
        self.foto_id = foto_id
        self.data_atualizacao = datetime.now()
        return self.foto_id

