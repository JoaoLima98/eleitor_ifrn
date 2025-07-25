from infra.models.eleitor_model import EleitorModel, StatusEnum
from infra.models.pessoa_model import PessoaModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from domain.eleitor import Eleitor
from domain.enum.status import Status

class EleitorRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, eleitor: Eleitor):
        try:
            pessoa_model = self.db.get(PessoaModel, eleitor.id)
            if not pessoa_model:
                raise ValueError("Pessoa associada ao eleitor não encontrada no banco.")

            model = EleitorModel(
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

    def buscar_por_id(self, eleitor_id: int) -> Eleitor | None:
        try:
            model = self.db.execute(
                select(EleitorModel).where(EleitorModel.id == eleitor_id)
            ).scalar_one_or_none()

            if model is None:
                return None

            pessoa_model = self.db.get(PessoaModel, model.id)
            if pessoa_model is None:
                return None

            return Eleitor(
                id=pessoa_model.id,
                nome=pessoa_model.nome,
                cpf=pessoa_model.cpf,
                email=pessoa_model.email,
                data_nascimento=pessoa_model.data_nascimento,
                status=Status(model.status),
                vinculos=[]  # carregar vínculos se necessário
            )
        except Exception as e:
            raise e
