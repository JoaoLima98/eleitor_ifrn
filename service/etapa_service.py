from repository.etapa_repository import EtapaRepository


etapa_repository = EtapaRepository()
class EtapaService:
    
    
    def get_etapa_and_turno_by_etapa_and_turno(self, etapa: int, turno: str):
        resultado = etapa_repository.get_etapa_and_turno_unicos(etapa, turno)
        if resultado:
            e, t = resultado
            return (e, t)
        return None