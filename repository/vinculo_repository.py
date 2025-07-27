from models.vinculo_model import VinculoModel
from models.curso_model import CursoModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from domain.curso import Curso
from domain.enum.tipo_vinculo import TipoVinculo
from infra.db import get_session

class VinculoRepository:
    def __init__(self, db: Session = get_session()):
        self.db = db

    def salvar(self, vinculo):
        model = VinculoModel(
            id=vinculo.id,
            tipo=vinculo.tipo.name,
            matricula=vinculo.matricula,
            pessoa_id=vinculo.id_pessoa,
            curso_id=vinculo.curso.id
        )
        try:
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return vinculo
        except Exception as e:
            self.db.rollback()
            raise e

    def buscar_por_id(self, vinculo_id: int):
        try:
            model = self.db.execute(
                select(VinculoModel).where(VinculoModel.id == vinculo_id)
            ).scalar_one_or_none()

            if model is None:
                return None

            curso_model = self.db.get(CursoModel, model.curso_id)

            curso = Curso(
                id=curso_model.id,
                nome=curso_model.nome,
                descricao=curso_model.descricao,
                etapa=None  # você pode carregar etapa se quiser aqui
            )

            return (
                model.id,
                model.matricula,
                TipoVinculo[model.tipo],
                model.pessoa_id,
                curso
            )
        except Exception as e:
            raise e

    def buscar_por_matricula(self, matricula: str):
        try:
            model = self.db.execute(
                select(VinculoModel).where(VinculoModel.matricula == matricula)
            ).scalar_one_or_none()

            if model is None:
                return None

            curso_model = self.db.get(CursoModel, model.curso_id)

            curso = Curso(
                id=curso_model.id,
                nome=curso_model.nome,
                descricao=curso_model.descricao,
                etapa=None
            )

            return (
                model.id,
                model.matricula,
                TipoVinculo[model.tipo],
                model.pessoa_id,
                curso
            )
        except Exception as e:
            raise e
