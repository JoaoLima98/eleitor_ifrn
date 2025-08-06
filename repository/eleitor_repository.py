from models import models
from domain.eleitor import Eleitor
from sqlalchemy import update
from sqlalchemy.orm import joinedload
from infra.db import SessionLocal  # SessionLocal é sessionmaker configurado

class EleitorRepository:

    def salvar(self, eleitor):
        try:
            with SessionLocal() as session:
                pessoa_model = session.get(models.PessoaModel, eleitor.id)
                if not pessoa_model:
                    raise ValueError("Pessoa associada ao eleitor não encontrada no banco.")

                model = models.EleitorModel(
                    id=eleitor.id,
                    status=eleitor.status.name
                )
                session.add(model)
                session.commit()
                session.refresh(model)
                return eleitor
        except Exception as e:
            # Se usar with, rollback ocorre automático em erro, mas se quiser explicitar:
            # session.rollback() -- só dentro do with, não aqui fora
            raise e

    def buscar_por_cpf(self, cpf: str):
        try:
            with SessionLocal() as session:
                model = session.query(models.PessoaModel)\
                    .options(joinedload(models.PessoaModel.vinculos))\
                    .filter(models.PessoaModel.cpf == cpf)\
                    .first()
                return model
        except Exception as e:
            raise e
    
    def atualizar(self, eleitor: Eleitor, eleitor_id: int):
        try:
            with SessionLocal() as session:
                result = session.execute(
                    update(models.EleitorModel)
                    .where(models.EleitorModel.id == eleitor_id)
                    .values(status=eleitor.status.name)
                )
                session.commit()
                return result
        except Exception as e:
            raise e
        
    def buscar_por_id(self, id: int):
        try:
            with SessionLocal() as session:
                model = session.get(models.EleitorModel, id)
                if model is None:
                    return None
                return model
        except Exception as e:
            raise e
        
    def remover(self, eleitor_id: int):
        try:
            with SessionLocal() as session:
                session.query(models.EleitorModel).filter(models.EleitorModel.id == eleitor_id).delete()
                session.commit()
        except Exception as e:
            raise e