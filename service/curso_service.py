
from repository.curso_repository import CursoRepository
from repository.etapa_repository import EtapaRepository

class CursoService:
    def __init__(self):
        self.curso_repository = CursoRepository()
        self.etapa_repository = EtapaRepository()

    def salvar(self, curso):
        # Verifica se a etapa existe
        if curso.etapa:
            etapa = self.etapa_repository.buscar_por_id(curso.etapa.etapa, curso.etapa.turno)
            if not etapa:
                raise ValueError("Etapa associada ao curso não encontrada.")
        
        return self.curso_repository.salvar(curso)

    def buscar_por_id(self, curso_id: int):
        return self.curso_repository.buscar_por_id(curso_id)

    def get_nome_by_nome(self, nome: str) -> bool:
        return self.curso_repository.get_nome_by_nome(nome)
