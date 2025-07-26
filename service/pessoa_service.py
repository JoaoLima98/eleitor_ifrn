from repository.pessoa_repository import PessoaRepository
from domain.pessoa import Pessoa
import re

repository = PessoaRepository()

class PessoaService:
  
    def __init__(self, repository: PessoaRepository):
        self.repository = repository
  
    def salvar(self, pessoa: Pessoa) -> Pessoa:
        if not self.validar_cpf(pessoa.cpf):
            raise ValueError("CPF inválido.")
        
        existente_cpf = self.repository.buscar_por_cpf(pessoa.cpf)
        if existente_cpf and existente_cpf.id != pessoa.id:
            raise ValueError("CPF já cadastrado.")

        existente_email = self.repository.buscar_por_email(pessoa.email)
        if existente_email and existente_email.id != pessoa.id:
            raise ValueError("Email já cadastrado.")

        return self.repository.salvar(pessoa)
      
    def buscar_por_cpf(self, cpf: str) -> Pessoa | None:
        if not self.validar_cpf(cpf):
            raise ValueError("CPF inválido.")
        return self.repository.buscar_por_cpf(cpf)
    
    def buscar_por_email(self, email: str) -> Pessoa | None:
        if not email:
            raise ValueError("Email inválido.")
        return self.repository.buscar_por_email(email)
      

    def validar_cpf(self, cpf: str):
      return self.__validar_cpf(cpf)
    
    def __validar_cpf(self, cpf: str) -> bool:
      
      cpf = re.sub(r"\D", "", cpf)  # Remove não-dígitos
      if len(cpf) != 11 or cpf == cpf[0] * 11:
          return False

      for i in range(9, 11):
          soma = sum(int(cpf[j]) * ((i+1) - j) for j in range(i))
          digito = (soma * 10 % 11) % 10
          if digito != int(cpf[i]):
              return False

      return True

