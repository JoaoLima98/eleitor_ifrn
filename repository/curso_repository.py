from models.curso_model import CursoModel
from sqlalchemy.orm import Session
from domain.etapa import Etapa
from infra.db import get_session

class CursoRepository:
    def __init__(self, db: Session = get_session()):
        self.db = db

    def salvar(self, curso):
        try:
            model = CursoModel(
                id=curso.id,
                nome=curso.nome,
                descricao=curso.descricao,
                etapa_id=curso.etapa.id if curso.etapa else None
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return curso
        except Exception as e:
            self.db.rollback()
            raise e

    def get_nome_by_nome(self, nome: str) -> bool:
        return self.db.query(CursoModel).filter(CursoModel.nome == nome).first() is None
    def buscar_por_id(self, curso_id: int):
        try:
            model = self.db.query(CursoModel).filter(CursoModel.id == curso_id).first()
            if model is None:
                return None

            etapa = Etapa(id=model.etapa_id) if model.etapa_id else None
            return (
                model.id,
                model.nome,
                model.descricao,
                etapa
            )
        except Exception as e:
            raise e