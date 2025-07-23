import unittest
from unittest.mock import patch
from domain.etapa import Etapa

class TestCurso(unittest.TestCase):
    
    def setUp(self):
        self.etapa = Etapa(7, "Noturno")

    
    def test_etapa_and_turno_unicos(self):
        resultado = self.etapa.verifica_etapa_and_turno_unicos()
        self.assertEqual(resultado, (7, "Noturno"))
    
    def test_etapa_nao_e_falsy(self):
        resultado = self.etapa.verifica_se_etapa_nao_e_falsy()
        self.assertTrue(resultado)

    def test_turno_nao_e_falsy(self):
        resultado = self.etapa.verifica_se_turno_nao_e_falsy()
        self.assertTrue(resultado)