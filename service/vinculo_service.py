from domain.vinculo import Vinculo
from repository.vinculo_repository import VinculoRepository
from repository.pessoa_repository import PessoaRepository
from repository.curso_repository import CursoRepository

class VinculoService:
    def __init__(
        self,
        vinculo_repository: VinculoRepository,
        pessoa_repository: PessoaRepository,
        curso_repository: CursoRepository
    ):
        self.vinculo_repository = vinculo_repository
        self.pessoa_repository = pessoa_repository
        self.curso_repository = curso_repository

    def salvar(self, vinculo: Vinculo) -> Vinculo:
        # Matrícula já existe?
        if self.vinculo_repository.buscar_por_matricula(vinculo.matricula):
            raise ValueError("Matrícula já cadastrada.")

        # Pessoa existe?
        pessoa = self.pessoa_repository.buscar_por_id(vinculo.id_pessoa)
        if not pessoa:
            raise ValueError("Pessoa associada ao vínculo não encontrada.")

        # Curso existe?
        curso = self.curso_repository.buscar_por_id(vinculo.curso.id)
        if not curso:
            raise ValueError("Curso associado ao vínculo não encontrado.")

        return self.vinculo_repository.salvar(vinculo)

    def buscar_por_id(self, vinculo_id: int) -> Vinculo | None:
        return self.vinculo_repository.buscar_por_id(vinculo_id)
