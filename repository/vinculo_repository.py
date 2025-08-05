from models import models
from domain.vinculo import Vinculo
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from domain.curso import Curso
from domain.enum.tipo_vinculo import TipoVinculo
from infra.db import SessionLocal

class VinculoRepository:

    def salvar(vinculo: Vinculo):
        """
        Cria ou atualiza um vínculo no banco de dados.

        Args:
            vinculo (Vinculo): Objeto Vinculo contendo os dados a serem salvos.

        Returns:
            models.VinculoModel: O objeto VinculoModel salvo ou atualizado.
        """
        db = SessionLocal()
        try:
            # Verifica se o vínculo já existe pela matrícula
            db_vinculo = db.query(models.VinculoModel).filter(models.VinculoModel.matricula == vinculo.matricula).first()

            if db_vinculo:
                # Atualiza o vínculo existente
                db_vinculo.tipo = vinculo.tipo
                db_vinculo.id_pessoa = vinculo.id_pessoa
                db_vinculo.curso_id = vinculo.curso_id
                
                db.commit()
                db.refresh(db_vinculo)
                return db_vinculo
            else:
                # Cria um novo vínculo
                novo_vinculo = models.VinculoModel(
                    matricula=vinculo.matricula,
                    tipo=vinculo.tipo,
                    id_pessoa=vinculo.id_pessoa,
                    curso_id=vinculo.curso_id
                )
                db.add(novo_vinculo)
                db.commit()
                db.refresh(novo_vinculo)
                return novo_vinculo
                
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()



    def buscar_por_matricula(self, matricula: str):
        try:
            with SessionLocal() as session:
                model = session.execute(
                    select(models.VinculoModel).where(models.VinculoModel.matricula == matricula)
                ).scalar_one_or_none()

                if model is None:
                    return None

                return Vinculo(
                    id=model.id,
                    matricula=model.matricula,
                    tipo=TipoVinculo(model.tipo),
                    id_pessoa=model.id_pessoa,
                    curso_id=model.curso_id
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

                return Vinculo(
                    id=model.id,
                    matricula=model.matricula,
                    tipo=TipoVinculo(model.tipo),
                    id_pessoa=model.id_pessoa,
                    curso_id=model.curso_id
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
                        id_pessoa=vinculo.id_pessoa,
                        curso_id=vinculo.curso.id
                    )
                )
                session.commit()

                model = session.query(models.VinculoModel)\
                    .options(joinedload(models.VinculoModel.curso))\
                    .filter_by(id=vinculo_id).one_or_none()

                if model is None:
                    raise Exception(f"Vínculo com id {vinculo_id} não encontrado para atualização.")

                return Vinculo(
                    id=model.id,
                    matricula=model.matricula,
                    tipo=TipoVinculo(model.tipo),
                    id_pessoa=model.id_pessoa,
                    curso_id=model.curso_id
                )

        except Exception as e:
            raise e


        
    def getVinculosByIdPessoa(self, id_pessoa):
        try:
            with SessionLocal() as session:
                result = session.execute(
                    select(models.VinculoModel).where(models.VinculoModel.id_pessoa == id_pessoa)
                )
                return result.scalars().all()
        except Exception as e:
            raise e
            
        
