
from repository.etapa_repository import EtapaRepository

class EtapaService:
    def __init__(self):
        self.etapa_repository = EtapaRepository()

    def salvar(self, etapa):
        if self.etapa_repository.buscar_por_id(etapa.id):
            raise ValueError("Etapa já cadastrada.")
        return self.etapa_repository.salvar(etapa)

    def atualizar(self, etapa, etapa_id):
        return self.etapa_repository.atualizar(etapa, etapa_id)
    def remover(self, etapa_id: int):
        return self.etapa_repository.remover(etapa_id)
