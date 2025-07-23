from repository.pessoa_repository import PessoaRepository
import re

pessoa_repository = PessoaRepository()

class PessoaService:
    
    def get_cpf_by_cpf(self, cpf: str):
        if not cpf:
          return False
        return pessoa_repository.get_cpf_unico(cpf)

    def get_email_by_email(self, email: str):
        if not email:
           return False
        return pessoa_repository.get_email_unico(email)
    
    
    
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

