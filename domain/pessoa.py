from datetime import date, datetime
from eleitor.domain.vinculo import Vinculo
from eleitor.service.pessoa_service import PessoaService
import re

class Pessoa:

    def __init__(self, id: int, cpf: str, email: str, data_nascimento: date, nome: str, vinculos = list[Vinculo], 
                 service = PessoaService()):
        self.id = id
        self.cpf = cpf
        self.email = email
        self.data_nascimento = data_nascimento
        self.nome = nome
        self.vinculos = vinculos or []
        self.data_criacao = datetime.now()
        self.data_atualizacao = datetime.now()
        self.service = service
        
        self.validar_vinculos()
        self.verifica_email_unico()
        self.verifica_cpf_unico()
        self.verifica_data_nascimento_nao_e_falsy()
        self.verifica_data_nascimento_valida()
        self.verifica_se_cpf_nao_e_falsy()
        self.verifica_se_nome_nao_e_falsy()
        self.verifica_se_email_nao_e_falsy()
        self.validar_email()
        if not self.valida_cpf():
            raise ValueError(f"CPF inválido: {self.cpf}")
        self.verifica_se_vinculo_nao_e_falsy()
        
        
    def verifica_data_nascimento_nao_e_falsy(self):
        if not bool(self.data_nascimento):
            raise ValueError("Data de nascimento inválido.")
        return True
    
    def verifica_cpf_unico(self):
        if not self.service.get_cpf_by_cpf(self.cpf):
            raise ValueError("CPF já cadastrado.")
        return self.cpf
    
    def verifica_email_unico(self):
        if not self.service.get_email_by_email(self.email):
            raise ValueError("Email já cadastrado.")
        return self.email

    def valida_cpf(self):
        if not self.cpf:
          return False
        if not self.verifica_cpf_unico():
            return False
        return self.service.validar_cpf(self.cpf)


    def validar_email(self):
        if not self.verifica_se_email_nao_e_falsy():
            return False    
            
        padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(padrao, self.email) is not None
    
    def verifica_se_email_nao_e_falsy(self):
        if not bool(self.email):
            raise ValueError("Email inválido.")
        return True
    
    
    def verifica_se_cpf_nao_e_falsy(self):
        if not bool(self.cpf):
            raise ValueError("CPF inválido.")
        return True
    
   
    def verifica_data_nascimento_valida(self):
        try:
            hoje = datetime.today().date()
            idade = (hoje - self.data_nascimento).days // 365
            return 0 <= idade <= 120
        except Exception:
            return False
    
    def verifica_se_nome_nao_e_falsy(self):
        if not bool(self.nome):
            raise ValueError("Nome inválido.")
        return True
    
    def validar_vinculos(self):
        if not self.vinculos or len(self.vinculos) == 0:
            raise ValueError("Pessoa deve ter pelo menos um vínculo.")
        for vinculo in self.vinculos:
            if vinculo.id_pessoa != self.id:
                raise ValueError(f"Vínculo {vinculo} não corresponde ao ID da pessoa.")
    
    def get_pessoa_id(self):
        return self.id
    
    def verifica_se_vinculo_nao_e_falsy(self):
        if not self.vinculos:
            raise ValueError("Pessoa não possui vínculos.")
        return True