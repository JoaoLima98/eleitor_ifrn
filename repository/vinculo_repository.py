from models import models
from domain.vinculo import Vinculo
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from domain.curso import Curso
from domain.enum.tipo_vinculo import TipoVinculo
from infra.db import SessionLocal

class VinculoRepository:

    def salvar(self, vinculo):
        try:
            with SessionLocal() as session:
                # Criação e persistência do vínculo
                model = models.VinculoModel(
                    id=vinculo.id,
                    matricula=vinculo.matricula,
                    tipo=vinculo.tipo.value,
                    pessoa_id=vinculo.id_pessoa,
                    curso_id=vinculo.curso.id
                )
                session.add(model)
                session.flush()
                session.commit()

                # Recarregar vínculo com curso usando joinedload
                model = session.query(models.VinculoModel)\
                    .options(joinedload(models.VinculoModel.curso))\
                    .filter_by(id=model.id).one()

                # Montagem do domínio Curso
                curso = Curso(
                    id=model.curso.id,
                    nome=model.curso.nome,
                    descricao=model.curso.descricao,
                    etapa=None  # Carregar etapa, se necessário
                )

                # Retorno do domínio Vinculo
                return Vinculo(
                    id=model.id,
                    matricula=model.matricula,
                    tipo=TipoVinculo(model.tipo),
                    pessoa_id=model.pessoa_id,
                    curso=curso
                )
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
                    tipo=TipoVinculo(model.tipo),
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
                    tipo=TipoVinculo(model.tipo),
                    pessoa_id=model.pessoa_id,
                    curso=curso
                )
        except Exception as e:
            raise e

    def remover(self, vinculo_id: int):
            try:
                with SessionLocal() as session:
                    session.query(models.VinculoModel).filter(models.VinculoModel.id == vinculo_id).delete()
                    session.commit()
            except Exception as e:
                raise e
    
    def remover_curso_do_vinculo(self, curso_id: int):
        try:
            with SessionLocal() as session:
                session.execute(
                    update(models.VinculoModel)
                    .where(models.VinculoModel.curso_id == curso_id)
                    .values(curso_id=None))
            session.commit()
        except Exception as e:
                raise e
    def atualizar(self, vinculo: Vinculo, vinculo_id: int):
        try:
            with SessionLocal() as session:
                session.execute(
                    update(models.VinculoModel)
                    .where(models.VinculoModel.id == vinculo_id)
                    .values(
                        matricula=vinculo.matricula,
                        tipo=vinculo.tipo.value,
                        pessoa_id=vinculo.id_pessoa,
                        curso_id=vinculo.curso.id
                    )
                )
                session.commit()

                model = session.query(models.VinculoModel)\
                    .options(joinedload(models.VinculoModel.curso))\
                    .filter_by(id=vinculo_id).one_or_none()

                if model is None:
                    raise Exception(f"Vínculo com id {vinculo_id} não encontrado para atualização.")

                curso = Curso(
                    id=model.curso.id,
                    nome=model.curso.nome,
                    descricao=model.curso.descricao,
                    etapa=None
                )

                return Vinculo(
                    id=model.id,
                    matricula=model.matricula,
                    tipo=TipoVinculo(model.tipo),
                    id_pessoa=model.pessoa_id,
                    curso=curso
                )

        except Exception as e:
            raise e


        
    def getVinculosByIdPessoa(self, pessoa_id):
        try:
            with SessionLocal() as session:
                result = session.execute(
                    select(models.VinculoModel).where(models.VinculoModel.pessoa_id == pessoa_id)
                )
                return result.scalars().all()
        except Exception as e:
            raise e
            
        
