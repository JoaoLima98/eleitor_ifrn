class Etapa:
    
    def __init__(self,id: int, etapa: int, turno: str):
        self.id = id
        self.etapa = etapa
        self.turno = turno
        self.verifica_se_etapa_nao_e_falsy()
        self.verifica_se_turno_nao_e_falsy()
    
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