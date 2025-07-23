from repository.curso_repository import CursoRepository


curso_repository = CursoRepository()
class CursoService:
    
    
    def get_nome_by_nome(self, nome: str) -> bool:
        if not nome:
           return False
        return curso_repository.get_nome_unico(nome)