from repository.vinculo_repository import VinculoRepository
from repository.pessoa_repository import PessoaRepository
from repository.curso_repository import CursoRepository

class VinculoService:
    def __init__(self):
        self.vinculo_repository = VinculoRepository()
        self.pessoa_repository = PessoaRepository()
        self.curso_repository = CursoRepository()

    def salvar(self, vinculos):
        salvos = []
        for vinculo in vinculos:
            if self.vinculo_repository.buscar_por_matricula(vinculo.matricula):
                raise ValueError("Matrícula já cadastrada.")

            pessoa = self.pessoa_repository.buscar_por_id(vinculo.id_pessoa)
            if not pessoa:
                raise ValueError("Pessoa associada ao vínculo não encontrada.")

            curso = self.curso_repository.buscar_por_id(vinculo.curso.id)
            if not curso:
                raise ValueError("Curso associado ao vínculo não encontrado.")

            salvo = self.vinculo_repository.salvar(vinculo)
            salvos.append(salvo)
        return salvos


    def buscar_por_id(self, vinculo_id: int):
        return self.vinculo_repository.buscar_por_id(vinculo_id)
