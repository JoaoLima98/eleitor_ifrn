from service.etapa_service import EtapaService

etapa_service = EtapaService()
class Etapa:
    
    def __init__(self, etapa: int, turno: str, service: EtapaService = etapa_service):
        self.etapa = etapa
        self.turno = turno
        self.service = service
        self.verifica_etapa_and_turno_unicos()
        self.verifica_se_etapa_nao_e_falsy()
        self.verifica_se_turno_nao_e_falsy()
    
    
    def verifica_etapa_and_turno_unicos(self):
        if self.service.get_etapa_and_turno_by_etapa_and_turno(self.etapa, self.turno):
            raise ValueError(f"A combinação etapa={self.etapa} e turno='{self.turno}' já existe.")
        return (self.etapa, self.turno)
    
    def verifica_se_etapa_nao_e_falsy(self):
        if not bool(self.etapa):
            raise ValueError("Etapainválido.")
        return True
    
    def verifica_se_turno_nao_e_falsy(self):
        if not bool(self.turno):
            raise ValueError("Turno inválido.")
        return True
    
    def __str__(self):
        return f"Etapa {self.etapa} - Turno: {self.turno}"