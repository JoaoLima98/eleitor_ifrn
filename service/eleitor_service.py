from repository.eleitor_repository import EleitorRepository

eleitor_repository = EleitorRepository()
class EleitorService:
        
    
    def get_lista_eleitores_ativos(self):
        lista_de_eleitores_ativos = eleitor_repository.get_lista_eleitores()
        return lista_de_eleitores_ativos