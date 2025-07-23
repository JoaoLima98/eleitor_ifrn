import unittest
from unittest.mock import patch
from domain.eleitor import Eleitor
from domain.enum.status import Status
from datetime import date

from domain.vinculo import Vinculo
from domain.curso import Curso
from service.eleitor_service import EleitorService

class TestEleitores(unittest.TestCase):

    def setUp(self):
        self.service = EleitorService()
        self.curso = Curso(1, "Filosofia", "Curso de licenciatura em Filosofia")
        vinculo1 = Vinculo(id=1, matricula="1234567", tipo=1, id_pessoa=123,curso=self.curso)
        self.eleitor = Eleitor(
                            id=123,
                            nome="João Silva",
                            email="joao@example.com",
                            cpf="24686548039",
                            data_nascimento=date(2000, 1, 1),
                            status=1,
                            vinculos=[vinculo1]
                        )
    
    def test_eleitor_initialization(self):
        self.assertEqual(self.eleitor.id, 123)
        self.assertEqual(self.eleitor.nome, "João Silva")
        self.assertEqual(self.eleitor.email, "joao@example.com")
        self.assertEqual(self.eleitor.cpf, "24686548039")
        self.assertEqual(self.eleitor.data_nascimento, date(2000, 1, 1))

    def test_eleitor_status(self):
        self.assertEqual(self.eleitor.status, Status.ATIVO)

    def test_set_eleitor_inativo(self):
        resultado = self.eleitor.set_eleitor_inativo()
        self.assertEqual(resultado, Status.INATIVO)
    
    def test_set_eleitor_suspenso(self):
        resultado = self.eleitor.set_eleitor_suspenso()
        self.assertEqual(resultado, Status.SUSPENSO)
    
    def test_set_eleitor_ativo(self):
        resultado = self.eleitor.set_eleitor_ativo()
        self.assertEqual(resultado, Status.ATIVO)
        
    def test_get_lista_eleitores_ativos(self):

        resultado = self.service.get_lista_eleitores_ativos()
        
        for eleitor in resultado:
            self.assertEqual(eleitor.status, Status.ATIVO)
            print(f"Eleitor: {eleitor.nome}, Status: {eleitor.status.name}")

        self.assertEqual(len(resultado), 2)
 
        

if __name__ == '__main__':
    unittest.main()