from domain.etapa import Etapa
from repository.etapa_repository import EtapaRepository

class EtapaService:
    def __init__(self, etapa_repository: EtapaRepository):
        self.etapa_repository = etapa_repository

    def salvar(self, etapa: Etapa) -> Etapa:
        if self.etapa_repository.get_etapa_and_turno_by_etapa_and_turno(etapa.etapa, etapa.turno):
            raise ValueError("A combinação etapa e turno já está cadastrada.")
        return self.etapa_repository.salvar(etapa)

    def buscar_por_id(self, etapa: int, turno: str) -> Etapa | None:
        return self.etapa_repository.buscar_por_id(etapa, turno)
