from repository.pessoa_repository import PessoaRepository
from domain.vinculo import Vinculo
import re

class PessoaService:
  
    def __init__(self):
        self.pessoa_repository = PessoaRepository()
  
    def salvar(self, pessoa):
        if not self.validar_cpf(pessoa.cpf):
            raise ValueError("CPF inválido.")
        
        existente_cpf = self.pessoa_repository.buscar_por_cpf(pessoa.cpf)
        if existente_cpf and existente_cpf.id != pessoa.id:
            raise ValueError("CPF já cadastrado.")

        existente_email = self.pessoa_repository.buscar_por_email(pessoa.email)
        if existente_email and existente_email.id != pessoa.id:
            raise ValueError("Email já cadastrado.")

        return self.pessoa_repository.salvar(pessoa)
      
    def buscar_por_cpf(self, cpf: str):
        if not self.validar_cpf(cpf):
            raise ValueError("CPF inválido.")
        return self.pessoa_repository.buscar_por_cpf(cpf)
    
    def buscar_por_id(self, id: int):
        if not id:
            raise ValueError("Pessoa inválido.")
        return self.pessoa_repository.buscar_por_id(id)
    
    def buscar_por_email(self, email: str):
        if not email:
            raise ValueError("Email não encontrado inválido.")
        return self.pessoa_repository.buscar_por_email(email)
    
    def atualizar(self, pessoa, id_pessoa):
            return self.pessoa_repository.atualizar(pessoa, id_pessoa)
    def remover(self, id_pessoa: int):
        return self.pessoa_repository.remover(id_pessoa)
    def adicionar_vinculo(self, id_pessoa: int, vinculo: Vinculo):
        return self.pessoa_repository.adicionar_vinculo(id_pessoa, vinculo)
      

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

