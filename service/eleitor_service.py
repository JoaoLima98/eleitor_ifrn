from repository.eleitor_repository import EleitorRepository
from domain.enum.status import Status
from repository.pessoa_repository import PessoaRepository
 
class EleitorService:
    def __init__(self):
        self.eleitor_repository = EleitorRepository()
        self.pessoa_repository = PessoaRepository()

    def salvar(self, eleitor):
        # Verifica se a pessoa existe, pelo id ou pelo cpf
        pessoa = self.pessoa_repository.buscar_por_cpf(eleitor.cpf)
        if not pessoa:
            raise ValueError("Pessoa associada ao eleitor não encontrada.")

        # Validar status
        if eleitor.status not in Status:
            raise ValueError("Status do eleitor inválido.")

        # Verificar duplicidade de eleitor (por id da pessoa)
        eleitor_existente = self.eleitor_repository.buscar_por_cpf(eleitor.cpf)
        if eleitor_existente and eleitor_existente.id != eleitor.id:
            raise ValueError("Eleitor com este CPF já cadastrado.")

        # Ajusta o id do eleitor para o id da pessoa existente (importante!)
        eleitor.id = pessoa.id

        # Salva eleitor (supondo que Pessoa já existe)
        return self.eleitor_repository.salvar(eleitor)
    def atualizar(self, eleitor, eleitor_id):
        return self.eleitor_repository.atualizar(eleitor, eleitor_id)
    def remover(self, eleitor_id: int):
        return self.eleitor_repository.remover(eleitor_id)