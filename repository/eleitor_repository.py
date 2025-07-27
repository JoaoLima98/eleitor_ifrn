from models import eleitor_model
from models import pessoa_model
from sqlalchemy import select
from sqlalchemy.orm import Session
from domain.enum.status import Status
from infra.db import get_session

class EleitorRepository:
    def __init__(self, db: Session = get_session()):
        self.db = db

    def salvar(self, eleitor):
        try:
            pessoa_model = self.db.get(pessoa_model, eleitor.id)
            if not pessoa_model:
                raise ValueError("Pessoa associada ao eleitor não encontrada no banco.")

            model = eleitor_model(
                id=eleitor.id,
                status=eleitor.status.name
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return eleitor
        except Exception as e:
            self.db.rollback()
            raise e

    def buscar_por_cpf(self, cpf: int):
        try:
            model = self.db.execute(
                select(eleitor_model).where(eleitor_model.cpf == cpf)
            ).scalar_one_or_none()

            if model is None:
                return None

            pessoa_model = self.db.get(pessoa_model, model.id)
            if pessoa_model is None:
                return None

            return (
                pessoa_model.id,
                pessoa_model.nome,
                pessoa_model.cpf,
                pessoa_model.email,
                pessoa_model.data_nascimento,
                Status(model.status),
                pessoa_model.vinculos
            )
                
            
        except Exception as e:
            raise e
