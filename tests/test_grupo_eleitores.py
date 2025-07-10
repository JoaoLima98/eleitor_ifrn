import unittest
from typing import List
from unittest.mock import patch
from eleitor.domain.eleitor import Eleitor
from eleitor.domain.vinculo import Vinculo
from eleitor.domain.curso import Curso
from eleitor.service.eleitor_service import EleitorService
from eleitor.domain.grupo_eleitores import GrupoEleitores

class TestGrupoEleitores(unittest.TestCase):

    def setUp(self):
        self.service = EleitorService()
        self.curso = Curso(1, "Filosofia", "Curso de licenciatura em Filosofia")
        vinculo1 = Vinculo(id=1, matricula="1234567", tipo=1, id_pessoa=123,curso=self.curso)
        self.eleitor = Eleitor(
                            id=123,
                            nome="João Silva",
                            email="joao@example.com",
                            cpf="24686548039",
                            data_nascimento="2000-01-01",
                            status=1,
                            vinculos=[vinculo1]
                        )
        self.grupo_eleitores = GrupoEleitores(1, "Eleitores TADS6m","Eleitores do curso de tads")
        self.lista = self.service.get_lista_eleitores_ativos()
        
        
    def test_set_lista_eleitores(self):
        resultado = self.grupo_eleitores.set_lista_eleitores(self.lista)
        self.assertEqual(resultado, self.lista)
    
    def test_append_lista_eleitores(self):
        resultado = self.grupo_eleitores.append_lista_eleitores(self.eleitor)
        self.assertEqual(resultado, self.eleitor)
        
    def test_remove_eleitor_da_lista(self):
        self.grupo_eleitores.append_lista_eleitores(self.eleitor)
        resultado = self.grupo_eleitores.remove_eleitor_da_lista(self.eleitor)
        self.assertEqual(resultado, self.eleitor)
    
    def test_get_lista_eleitores(self):
        self.grupo_eleitores.append_lista_eleitores(self.eleitor)
        resultado = self.grupo_eleitores.get_lista_eleitores()
        self.assertEqual(resultado, [self.eleitor])
        
    def test_inativa_grupo(self):
        #DESATIVAR O GRUPO
        resultado = self.grupo_eleitores.ativa_inativa_grupo()
        self.assertFalse(resultado)
    
    def test_ativa_grupo(self):
        #ATIVAR O GRUPO
        self.grupo_eleitores.ativo = False
        resultado = self.grupo_eleitores.ativa_inativa_grupo()
        self.assertTrue(resultado)
        
    def test_nome_nao_e_falsy(self):
        resultado = self.grupo_eleitores.verifica_se_nome_nao_e_falsy()
        self.assertTrue(resultado)

    def test_nome_unico(self):
        resultado = self.grupo_eleitores.verifica_nome_unico()
        self.assertEqual(resultado, "Eleitores TADS6m")