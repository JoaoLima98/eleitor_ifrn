from domain.pessoa import Pessoa
from datetime import date, datetime
from domain.enum.status import Status
from domain.vinculo import Vinculo


class Eleitor(Pessoa):
    
    def __init__(self, id: int, nome: str, email: str, cpf: str, data_nascimento: str, status: int, vinculos: list[Vinculo]):
        super().__init__(
            id=id,
            cpf=cpf,
            email=email,
            data_nascimento=data_nascimento,
            nome=nome,
            vinculos=vinculos
        )
        self.id = id
        self.status = Status(status)
        self.data_cadastro = datetime.now()
        self.data_atualizacao = datetime.now()
        
        
    def set_eleitor_inativo(self):
        self.status = Status.INATIVO
        return self.status
    
    def set_eleitor_suspenso(self):
        self.status = Status.SUSPENSO
        return self.status
    
    def set_eleitor_ativo(self):
        self.status = Status.ATIVO
        return self.status

