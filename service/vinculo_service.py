
from eleitor.repository.vinculo_repository import VinculoRepository

vinculo_repository = VinculoRepository()

class VinculoService:

  def get_matricula_by_matricula(self, matricula: str):
        if not matricula:
            return False
        return vinculo_repository.get_matricula_unica(matricula)