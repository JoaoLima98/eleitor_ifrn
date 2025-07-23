import unittest
from unittest.mock import patch
from domain.vinculo import Vinculo
from domain.enum.tipo_vinculo import TipoVinculo
from domain.curso import Curso
from domain.etapa import Etapa

class TestVinculo(unittest.TestCase):

    def setUp(self):
        self.etapa = Etapa(1, "Noturno")
        self.curso = Curso(1, "Filosofia", "Curso de licenciatura em Filosofia")
        self.vinculo_discente = Vinculo(1, "20231134040016", 1, 3, self.curso)
        self.vinculo_docente = Vinculo(2, "1234562", 2, 2, self.curso)
        #self.vinculo_invalido = Vinculo(3, "123", 1, 1, self.curso)

    def test_tipo_valido_discente(self):
        self.assertEqual(self.vinculo_discente.tipo, TipoVinculo.DISCENTE)

    def test_tipo_valido_docente(self):
        self.assertEqual(self.vinculo_docente.tipo, TipoVinculo.DOCENTE)
    
    def test_matricula_valida_discente(self):
        self.assertEqual(self.vinculo_discente.validar_matricula(), "20231134040016")

    def test_matricula_valida_docente(self):
        self.assertEqual(self.vinculo_docente.validar_matricula(), "1234562")

    def test_tipo_invalido(self):
        with self.assertRaises(ValueError):
            Vinculo(id=1,matricula="20231134040016", 
                    tipo=99, 
                    id_pessoa=2, 
                    curso=Curso(1, "Filosofia", "Curso de licenciatura em Filosofia"))

    '''def test_matricula_invalida(self):
        with self.assertRaises(ValueError):
            self.vinculo_invalido.validar_matricula()'''    

    def test_matricula_nao_e_falsy(self):
        self.assertTrue(self.vinculo_discente.verifica_se_matricula_nao_e_falsy())

    def test_tipo_nao_e_falsy(self):
        self.assertTrue(self.vinculo_discente.verifica_se_tipo_nao_e_falsy())

    def test_matricula_unica(self):
        resultado = self.vinculo_discente.verifica_matricula_unica()
        self.assertEqual(resultado, "20231134040016")


    def test_verifica_se_id_pessoa_nao_e_falsy(self):
        resultado = self.vinculo_discente.verifica_se_id_pessoa_nao_e_falsy()
        self.assertEqual(resultado, 3)
