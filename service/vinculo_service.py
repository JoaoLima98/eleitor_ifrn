from repository.vinculo_repository import VinculoRepository
from repository.pessoa_repository import PessoaRepository
from repository.curso_repository import CursoRepository

class VinculoService:
    def __init__(self):
        self.vinculo_repository = VinculoRepository()
        self.pessoa_repository = PessoaRepository()
        self.curso_repository = CursoRepository()

    def salvar(self, vinculo):
        lista_vinculos = self.vinculo_repository.getVinculosByIdPessoa(vinculo.id_pessoa)

        for vinculo_na_lista in lista_vinculos:
            if self.vinculo_repository.buscar_por_matricula(vinculo_na_lista.matricula):
                raise ValueError("Matrícula já cadastrada.")

            pessoa = self.pessoa_repository.buscar_por_id(vinculo_na_lista.id_pessoa)
            if not pessoa:
                raise ValueError("Pessoa associada ao vínculo não encontrada.")

            curso = self.curso_repository.buscar_por_id(vinculo_na_lista.curso.id)
            if not curso:
                raise ValueError("Curso associado ao vínculo não encontrado.")

        return self.vinculo_repository.salvar(vinculo)
        


    def buscar_por_id(self, vinculo_id: int):
        return self.vinculo_repository.buscar_por_id(vinculo_id)
    def atualizar(self, vinculo, vinculo_id):
        return self.vinculo_repository.atualizar(vinculo, vinculo_id)
    def remover(self, vinculo_id: int):
        return self.vinculo_repository.remover(vinculo_id)
    def remover_curso_do_vinculo(self, curso_id: int):
        return self.vinculo_repository.remover_curso_do_vinculo(curso_id)
        