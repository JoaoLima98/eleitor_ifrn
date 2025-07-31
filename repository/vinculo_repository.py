from models import models
from domain.vinculo import Vinculo
from sqlalchemy import select
from domain.curso import Curso
from domain.enum.tipo_vinculo import TipoVinculo
from infra.db import SessionLocal

class VinculoRepository:

    def salvar(self, vinculo):
        try:
            with SessionLocal() as session:
                model = models.VinculoModel(
                    id=vinculo.id,
                    matricula=vinculo.matricula,
                    tipo=vinculo.tipo,
                    pessoa_id=vinculo.id_pessoa,
                    curso_id=vinculo.curso.id
                )
                session.add(model)
                session.flush()
                session.refresh(model)
                session.commit()
                return model
        except Exception as e:
            raise e


    def buscar_por_matricula(self, matricula: str):
        try:
            with SessionLocal() as session:
                model = session.execute(
                    select(models.VinculoModel).where(models.VinculoModel.matricula == matricula)
                ).scalar_one_or_none()

                if model is None:
                    return None

                curso_model = session.get(models.CursoModel, model.curso_id)

                curso = Curso(
                    id=curso_model.id,
                    nome=curso_model.nome,
                    descricao=curso_model.descricao,
                    etapa=None  # Carregar etapa se desejar
                )

                return Vinculo(
                    id=model.id,
                    matricula=model.matricula,
                    tipo=TipoVinculo[model.tipo],
                    pessoa_id=model.pessoa_id,
                    curso=curso
                )
        except Exception as e:
            raise e
        
    def buscar_por_id(self, vinculo_id: int):
        try:
            with SessionLocal() as session:
                model = session.execute(
                    select(models.VinculoModel).where(models.VinculoModel.id == vinculo_id)
                ).scalar_one_or_none()

                if model is None:
                    return None

                curso_model = session.get(models.CursoModel, model.curso_id)

                curso = Curso(
                    id=curso_model.id,
                    nome=curso_model.nome,
                    descricao=curso_model.descricao,
                    etapa=None  # Carregar etapa se quiser
                )

                return Vinculo(
                    id=model.id,
                    matricula=model.matricula,
                    tipo=TipoVinculo[model.tipo],
                    pessoa_id=model.pessoa_id,
                    curso=curso
                )
        except Exception as e:
            raise e
