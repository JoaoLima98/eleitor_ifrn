from models import models
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
    