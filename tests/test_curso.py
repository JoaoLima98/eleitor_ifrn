import unittest
from unittest.mock import patch
from eleitor.domain.curso import Curso
from eleitor.domain.etapa import Etapa

class TestCurso(unittest.TestCase):
    
    def setUp(self):
        self.etapa = Etapa(1, "Noturno")
        self.curso = Curso(1, "Filosofia", "Curso de licenciatura em Filosofia")
        
    def test_definir_etapa(self):
        resultado = self.curso.definir_etapa(self.etapa)
        self.assertEqual(resultado, self.etapa)

    
    def test_nome_unico(self):
        resultado = self.curso.verifica_nome_unico()
        self.assertEqual(resultado, "Filosofia")
    
    def test_descricao_nao_e_falsy(self):
        resultado = self.curso.descricao_nao_e_falsy()
        self.assertTrue(resultado)
        
    def test_nome_nao_e_falsy(self):
        resultado = self.curso.nome_nao_e_falsy()
        self.assertTrue(resultado)