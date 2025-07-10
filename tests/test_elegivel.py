import unittest
from unittest.mock import patch
from datetime import date
from eleitor.domain.vinculo import Vinculo
from eleitor.domain.elegivel import Elegivel
from eleitor.domain.curso import Curso

class TestElegivel(unittest.TestCase):

    def setUp(self):

        self.curso = Curso(1, "Filosofia", "Curso de licenciatura em Filosofia")
        vinculo1 = Vinculo(id=1, matricula="1234567", tipo=1, id_pessoa=123,curso=self.curso)
        self.eleitor = Elegivel(
                            id=123,
                            nome="João Silva",
                            email="joao@example.com",
                            cpf="24686548039",
                            data_nascimento=date(2000, 1, 1),
                            foto_id =1,
                            vinculos=[vinculo1]
                        )
        
    '''def test_foto_nao_e_falsy(self):
        self.eleitor.foto = "foto.jpg"
        self.assertTrue(self.eleitor.verifica_se_foto_nao_e_falsy())'''
        
    def test_adicionar_foto(self):
        foto_id = 1
        self.eleitor.adicionar_foto(foto_id)
        self.assertEqual(self.eleitor.foto_id, foto_id)
        
        