
from repository.etapa_repository import EtapaRepository

class EtapaService:
    def __init__(self):
        self.etapa_repository = EtapaRepository()

    def salvar(self, etapa):
        if self.etapa_repository.buscar_por_id(etapa.id):
            raise ValueError("Etapa já cadastrada.")
        return self.etapa_repository.salvar(etapa)

    def buscar_por_id(self, etapa: int, turno: str):
        return self.etapa_repository.buscar_por_id(etapa, turno)
