from eleitor.domain.enum.status import Status
from datetime import date
from eleitor.domain.eleitor import Eleitor  # ou onde estiver sua classe Eleitor
from eleitor.domain.vinculo import Vinculo
from eleitor.domain.curso import Curso
class EleitorRepository:
    
    def get_lista_eleitores(self) -> list[Eleitor]:
        # Suponha que esse seja o retorno do banco
        self.curso = Curso(1, "Filosofia", "Curso de licenciatura em Filosofia")
        vinculo1 = Vinculo(id=1, matricula="1234560", tipo=1, id_pessoa=123,curso=self.curso)
        vinculo2 = Vinculo(id=2, matricula="1234568", tipo=1, id_pessoa=124,curso=self.curso)
        vinculo3 = Vinculo(id=3, matricula="1234569", tipo=1, id_pessoa=125,curso=self.curso)
        eleitores_do_banco = [
            Eleitor(123, "Ana", "ana@example.com", "24686548039", date(1990, 1, 1), 1, vinculos=[vinculo1]),  # ATIVO
            Eleitor(124, "Bruno", "bruno@example.com", "24686548039", date(1985, 5, 5), 2, vinculos=[vinculo2]),  # INATIVO
            Eleitor(125, "Clara", "clara@example.com", "24686548039", date(1992, 8, 10), 1, vinculos=[vinculo3]),  # ATIVO
        ]

        return [eleitor for eleitor in eleitores_do_banco if eleitor.status == Status.ATIVO]