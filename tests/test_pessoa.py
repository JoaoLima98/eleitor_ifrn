import unittest
from unittest.mock import patch, MagicMock
from domain.pessoa import Pessoa
from repository.pessoa_repository import PessoaRepository
from datetime import date
from domain.curso import Curso
from domain.vinculo import Vinculo


class TestPessoa(unittest.TestCase):

    pessoa_path = 'eleitor.domain.pessoa.PessoaService'
    
    def setUp(self):
        self.repositorio_mock = MagicMock(spec=PessoaRepository)
        self.service_mock = MagicMock()
        
        self.curso = Curso(1, "Filosofia", "Curso de licenciatura em Filosofia")
        vinculo = Vinculo(id=1, matricula="1234544", tipo=1, id_pessoa=1, curso=self.curso)
        self.pessoa = Pessoa(1, '11568675410', 'joaodo@example.com', date(1998,12,1), 'João da Silva', vinculos=[vinculo])
        ''' self.pessoa_invalida = self.service.criar_pessoa(1,'', 'joaogmailcom', date(1905,2,2), '', vinculos=[vinculo])'''
        self.pessoa.service = self.service_mock

    
    def test_valida_cpf(self):
        resultado = self.pessoa.valida_cpf()
        self.assertTrue(resultado)
    
    @patch(f"{pessoa_path}.get_cpf_by_cpf")
    def test_cpf_unico(self, mock_get_cpf_by_cpf):
        mock_get_cpf_by_cpf.return_value = None
        resultado = self.pessoa.verifica_cpf_unico()
        self.assertEqual(resultado, '11568675410')

    @patch(f"{pessoa_path}.get_email_by_email")
    def test_email_unico(self, mock_get_email_by_email):
        mock_get_email_by_email.return_value = None
        resultado = self.pessoa.verifica_email_unico()
        self.assertEqual(resultado, 'joaodo@example.com')
    
    def test_cpf_nao_e_falsy(self):
        resultado = self.pessoa.verifica_se_cpf_nao_e_falsy()
        self.assertTrue(resultado)
        
    '''def test_cpf_falsy(self):
        resultado = self.pessoa_invalida.verifica_data_nascimento_nao_e_falsy()
        self.assertFalse(resultado) '''   
    
    def test_email_nao_e_falsy(self):
        resultado = self.pessoa.verifica_se_email_nao_e_falsy()
        self.assertTrue(resultado)
    
    def test_data_nascimento_valida(self):
        resultado = self.pessoa.verifica_data_nascimento_valida()
        self.assertTrue(resultado)

    def test_nome_nao_e_falsy(self):
        resultado = self.pessoa.verifica_se_nome_nao_e_falsy()
        self.assertTrue(resultado)

    def test_data_nascimento_nao_e_falsy(self):
        resultado = self.pessoa.verifica_data_nascimento_nao_e_falsy()
        self.assertTrue(resultado)

    def test_email_valido(self):
        resultado = self.pessoa.validar_email()
        self.assertTrue(resultado)
    
        
    def test_criar_pessoa_com_vinculos(self):
        vinculo1 = Vinculo(id=1, matricula="1234565", tipo=1, id_pessoa=1, curso=self.curso)
        vinculo2 = Vinculo(id=2, matricula="20230000000001", tipo=2, id_pessoa=1, curso=self.curso)

        pessoa = Pessoa(
            id=1,
            cpf='11568675410',
            email='joaodo@example.com',
            data_nascimento=date(1998,12,1),
            nome='João da Silva',
            vinculos=[vinculo1, vinculo2]
        )
        
        self.assertEqual(len(pessoa.vinculos), 2)
        self.assertTrue(all(v.id_pessoa == pessoa.id for v in pessoa.vinculos))
    
    def test_get_id_pessoa(self):
        resultado = self.pessoa.get_id_pessoa()
        self.assertEqual(resultado, 1)

    def test_cpf_ja_cadastrado_com_service_mock(self):
        service_mock = MagicMock()
        service_mock.get_cpf_by_cpf.return_value = None  # CPF já cadastrado

        self.curso = Curso(1, "Filosofia", "Curso de licenciatura em Filosofia")
        vinculo = Vinculo(id=1, matricula="1234544", tipo=1, id_pessoa=1, curso=self.curso)

        with self.assertRaises(ValueError):
            Pessoa(
                id=1,
                cpf='11568675410',
                email='joaodo@example.com',
                data_nascimento=date(1998, 12, 1),
                nome='João da Silva',
                vinculos=[vinculo],
                service=service_mock
            )
    def test_vinculos_nao_e_falsy(self):
        resultado = self.pessoa.verifica_se_vinculo_nao_e_falsy()
        self.assertTrue(resultado)