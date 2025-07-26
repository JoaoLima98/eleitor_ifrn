from domain.grupo_eleitores import GrupoEleitores
from repository.grupo_eleitores_repository import GrupoEleitoresRepository

class GrupoEleitoresService:
    def __init__(self, grupo_repository: GrupoEleitoresRepository):
        self.grupo_repository = grupo_repository

    def salvar(self, grupo: GrupoEleitores) -> GrupoEleitores:
        if self.grupo_repository.nome_existe(grupo.nome):
            raise ValueError("Já existe um grupo com esse nome.")
        return self.grupo_repository.salvar(grupo)

    def buscar_por_id(self, grupo_id: int) -> GrupoEleitores | None:
        return self.grupo_repository.buscar_por_id(grupo_id)

    def buscar_por_nome(self, nome: str) -> GrupoEleitores | None:
        return self.grupo_repository.buscar_por_nome(nome)

    def adicionar_eleitor(self, grupo_id: int, eleitor) -> GrupoEleitores:
        grupo = self.grupo_repository.buscar_por_id(grupo_id)
        if not grupo:
            raise ValueError("Grupo não encontrado.")
        
        grupo.append_lista_eleitores(eleitor)
        return self.grupo_repository.salvar(grupo)
    def remover_eleitor(self, grupo_id: int, eleitor) -> GrupoEleitores:
        grupo = self.grupo_repository.buscar_por_id(grupo_id)
        if not grupo:
            raise ValueError("Grupo não encontrado.")
        
        grupo.remove_lista_eleitores(eleitor)
        return self.grupo_repository.salvar(grupo)
    def ativa_inativa_grupo(self, grupo_id: int) -> bool:
        grupo = self.grupo_repository.buscar_por_id(grupo_id)
        if not grupo:
            raise ValueError("Grupo não encontrado.")
        
        grupo.ativa_inativa_grupo()
        return self.grupo_repository.salvar(grupo).ativo
    def get_lista_eleitores(self, grupo_id: int) -> list:
        grupo = self.grupo_repository.buscar_por_id(grupo_id)
        if not grupo:
            raise ValueError("Grupo não encontrado.")
        
        return grupo.get_lista_eleitores()