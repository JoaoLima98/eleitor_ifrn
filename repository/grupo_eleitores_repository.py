class GrupoEleitoresRepository:
    
    def get_nome_unico(self, nome: str):
        lista_de_nomes = [
            "TADS2v",
            "TPQ4v"
        ]
        if nome in lista_de_nomes:
            return None
        return nome