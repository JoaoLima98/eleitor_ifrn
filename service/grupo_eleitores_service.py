from repository.grupo_eleitores_repository import GrupoEleitoresRepository


grupo_eleitores_repository = GrupoEleitoresRepository()
class GrupoEleitoresService:
    
    
    def get_nome_by_nome(self, nome: str) -> bool:
        if not nome:
           return False
        return grupo_eleitores_repository.get_nome_unico(nome)