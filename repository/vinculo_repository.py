class VinculoRepository:
    def get_matricula_unica(self, matricula: str):
        lista_de_matriculas = [
            "20230000000000",
            "1234512",
        ]
        if matricula in lista_de_matriculas:
            return None
        return matricula