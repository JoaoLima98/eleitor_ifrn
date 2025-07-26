from domain.enum.tipo_vinculo import TipoVinculo
from domain.curso import Curso



class Vinculo:
    def __init__(self, id: int, matricula: str, tipo: int, id_pessoa: int, curso: Curso):
        self.id = id
        self.matricula = matricula
        self.tipo = TipoVinculo(tipo)
        self.id_pessoa = id_pessoa
        self.curso = curso
        
        self.verifica_matricula_unica()
        self.validar_matricula()
        self.verifica_se_matricula_nao_e_falsy()
        self.verifica_se_tipo_nao_e_falsy()
        self.verifica_se_id_pessoa_nao_e_falsy()
        self.verifica_se_tipo_nao_e_falsy()
        
    def validar_matricula(self):
        if len(self.matricula) not in (14, 7):
            raise ValueError("Matrícula inválida. Deve ter 14 caracteres para discentes e 7 para docentes.")
        if not self.matricula.isdigit():
            raise ValueError("Matrícula inválida. Deve conter apenas números.")
        return self.matricula

    def verifica_se_matricula_nao_e_falsy(self):
        if not bool(self.matricula):
            raise ValueError("Matricula inválido.")
        return True
    
    def verifica_se_tipo_nao_e_falsy(self):
        if not bool(self.tipo):
            raise ValueError("Tipo inválido.")
        return True
    
    def verifica_se_id_pessoa_nao_e_falsy(self):
        if not self.id_pessoa:
            raise ValueError("ID da pessoa não pode ser vazio.")
        return self.id_pessoa
    
    


    def __str__(self):
        return f"Vinculo(matricula={self.matricula}, tipo={self.tipo.name})"