from domain.grupo_eleitores import GrupoEleitores
from repository.grupo_eleitores_repository import GrupoEleitoresRepository
from domain.eleitor import Eleitor

class GrupoEleitoresService:
    def __init__(self):
        self.grupo_repository = GrupoEleitoresRepository()

    def salvar(self, grupo: GrupoEleitores):
        print(f"Salvando grupo no serviço: ID={grupo.id}, Nome={grupo.nome}")
        
        try:
            # Chama o repositório para salvar
            salvo = self.grupo_repository.salvar(grupo)
            print(f"Grupo salvo no repositório: ID={salvo.id}, Nome={salvo.nome}")
            
            # Retorna o objeto atualizado
            return salvo
        except Exception as e:
            print(f"Erro ao salvar grupo no serviço: {str(e)}")
            raise e

    def buscar_por_id(self, grupo_id: int) -> GrupoEleitores | None:
        return self.grupo_repository.buscar_por_id(grupo_id)

    def buscar_por_nome(self, nome: str) -> GrupoEleitores | None:
        return self.grupo_repository.buscar_por_nome(nome)

    def adicionar_eleitor(self, grupo_id: int, eleitor) -> GrupoEleitores:
        grupo = self.grupo_repository.buscar_por_id(grupo_id)
        if not grupo:
            raise ValueError("Grupo não encontrado.")
        
        return self.grupo_repository.adicionar_eleitor(grupo_id, eleitor)

    
    def remover_eleitor(self, grupo_id: int, eleitor) -> GrupoEleitores:
        grupo = self.grupo_repository.buscar_por_id(grupo_id)
        if not grupo:
            raise ValueError("Grupo não encontrado.")
        
        return self.grupo_repository.remover_eleitor(grupo_id, eleitor)
    def ativa_inativa_grupo(self, grupo_id: int) -> bool:
        grupo_buscado = self.grupo_repository.buscar_por_id(grupo_id)
        grupo = GrupoEleitores(id=grupo_buscado.id, nome=grupo_buscado.nome, descricao=grupo_buscado.descricao, ativo=grupo_buscado.ativo, lista_eleitores=grupo_buscado.lista_eleitores)
        if not grupo:
            raise ValueError("Grupo não encontrado.")        
        
        grupo.ativa_inativa_grupo()
        atualizado = self.grupo_repository.atualizar(grupo, grupo_id)
        return bool(atualizado.ativo)
    
    def get_lista_eleitores(self, grupo_id: int) -> list:
        grupo = self.grupo_repository.buscar_por_id(grupo_id)
        if not grupo:
            raise ValueError("Grupo não encontrado.")
        
        return grupo
    
    def atualizar(self, grupo, grupo_id):
        return self.grupo_repository.atualizar(grupo, grupo_id)
    
    def remover(self, grupo_id: int):
        return self.grupo_repository.remover(grupo_id)
    
    def listar_eleitores_por_grupo_id(self, grupo_id: int) -> list[Eleitor]:
        eleitores = self.grupo_repository.listar_eleitores_por_grupo_id(grupo_id)

        for eleitor in eleitores:
            print(eleitor.nome)
        return eleitores
    
    def listar_todos_os_grupos(self):
        lista = self.grupo_repository.listar_grupos()
        return lista