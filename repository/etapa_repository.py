

class EtapaRepository:
    
    def __init__(self):
        # dados brutos, sem importar Etapa
        self._etapas = [
            (1, "Matutino"),
            (2, "Vespertino"),
            (3, "Noturno"),
            (4, "Integral"),
            (5, "Híbrido"),
            (6, "Online"),
            (7, "Especial")
        ]

    def get_etapa_and_turno_unicos(self, etapa: int, turno: str):
        for e, t in self._etapas:
            if e == etapa and t == turno:
                return (e, t)
        return None