class CursoRepository:
    
    def get_nome_unico(self, nome: str):
        lista_de_nomes = [
            "TADS",
            "TPQ"
        ]
        if nome in lista_de_nomes:
            return None
        return nome